#!/usr/bin/env python3
"""End-to-end test for the Headroom MCP compression server.

Drives the project's `.mcp.json` Headroom server over stdio exactly like Claude
Code does (real MCP client, not a raw JSON-RPC pipe), and asserts:

  1. The server exposes headroom_compress / headroom_retrieve / headroom_stats.
  2. Compressing a verbose JSON payload yields a meaningful token saving.
  3. The result carries a retrieval `hash`.
  4. headroom_retrieve(hash) round-trips the *exact* original content.
  5. headroom_stats reflects the compression that just happened.

No proxy is required - the on-demand MCP tools use a local store.

Run via `./headroom-test.sh` (which selects the venv interpreter). Exits 0 on
success, non-zero with a one-line diagnostic on the first failed check.

Checks return an error string rather than raising, so a failure unwinds the MCP
client cleanly instead of surfacing as an anyio ExceptionGroup traceback.
"""
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJ = Path(__file__).resolve().parent.parent
HEADROOM = PROJ / ".headroom-venv" / "bin" / "headroom"

# A realistic, highly-compressible payload: a uniform array of structured log
# records (the shape of server tool output / sweep results Headroom targets).
RECORDS = [
    {
        "ts": f"2026-08-11T17:{i // 60:02d}:{i % 60:02d}Z",
        "level": "INFO",
        "event": "sweep_result",
        "run_id": f"run-{i}",
        "stage": "stage2_6",
        "latency_ms": 11 + (i % 7),
        "ok": True,
    }
    for i in range(150)
]
PAYLOAD = json.dumps(RECORDS, indent=2)

# Observed ~39-60% for this payload depending on content variance; 30% leaves a
# comfortable margin while still proving real compression (not a pass-through).
MIN_SAVINGS_PCT = 30.0


async def run() -> Optional[str]:
    """Return None on success, or a one-line failure message."""
    if not HEADROOM.exists():
        return f"headroom binary not found at {HEADROOM} - is .headroom-venv installed?"

    params = StdioServerParameters(command=str(HEADROOM), args=["mcp", "serve"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1. Tools present
            names = {t.name for t in (await session.list_tools()).tools}
            print(f"  tools: {sorted(names)}")
            missing = {"headroom_compress", "headroom_retrieve", "headroom_stats"} - names
            if missing:
                return f"missing tool(s): {sorted(missing)}"

            # 2 + 3. Compress yields savings and a hash
            cres = await session.call_tool("headroom_compress", {"content": PAYLOAD})
            cdata = json.loads(cres.content[0].text)
            if cres.isError:
                return f"headroom_compress returned an error: {cdata}"
            savings = float(cdata.get("savings_percent", 0))
            h = cdata.get("hash")
            print(
                f"  compress: {cdata.get('original_tokens')} -> "
                f"{cdata.get('compressed_tokens')} tokens "
                f"({savings:.1f}% saved, hash={h})"
            )
            if savings < MIN_SAVINGS_PCT:
                return f"savings {savings:.1f}% below threshold {MIN_SAVINGS_PCT}%"
            if not h:
                return f"no retrieval hash in compress result: keys={list(cdata)}"

            # 4. Retrieve round-trips the exact original
            rres = await session.call_tool("headroom_retrieve", {"hash": h})
            rdata = json.loads(rres.content[0].text)
            if rres.isError:
                return f"headroom_retrieve returned an error: {rdata}"
            original = rdata.get("original_content")
            if original != PAYLOAD:
                return (
                    "retrieved content does not match original "
                    f"(got {len(original or '')} chars, expected {len(PAYLOAD)})"
                )
            print(f"  retrieve: exact round-trip OK (source={rdata.get('source')})")

            # 5. Stats reflect the compression.
            # Output shape depends on whether a Headroom proxy is reachable: with
            # no proxy it's a JSON object, with one it's a human-readable report
            # ("MCP Tool: N compressions, M tokens saved"). Accept both.
            sres = await session.call_tool("headroom_stats", {})
            stext = sres.content[0].text
            try:
                sdata = json.loads(stext)
                compressions = int(sdata.get("compressions", 0))
                saved = sdata.get("total_tokens_saved")
            except json.JSONDecodeError:
                m = re.search(
                    r"MCP Tool:\s*([\d,]+)\s*compressions?,\s*([\d,]+)\s*tokens saved",
                    stext,
                )
                if not m:
                    return f"stats output not recognised as JSON or report: {stext[:200]!r}"
                compressions = int(m.group(1).replace(",", ""))
                saved = m.group(2)
            if compressions < 1:
                return f"stats show no compressions: {stext[:200]!r}"
            print(f"  stats: {compressions} compression(s), {saved} tokens saved")

    return None


def main() -> None:
    try:
        err = asyncio.run(asyncio.wait_for(run(), timeout=60))
    except asyncio.TimeoutError:
        err = "timed out after 60s talking to the Headroom MCP server"

    if err:
        print(f"\n  FAIL: {err}")
        sys.exit(1)
    print("\n  PASS: Headroom MCP compression working end-to-end.")


if __name__ == "__main__":
    main()
