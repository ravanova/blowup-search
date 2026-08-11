# Headroom - AI context compression (MCP)

[Headroom](https://github.com/headroomlabs-ai/headroom) compresses large text
(tool output, logs, JSON, search results, file contents) before it's reasoned
over by an LLM - "60–95% fewer tokens, same answers". It's wired into this
project as a **project-scoped MCP server**, so Claude Code can compress big
blobs on demand and retrieve the originals later by hash.

This is dev tooling for working *on* Unsolved with Claude Code. It is **not**
part of the research pipeline itself and doesn't affect any experiment output.

## What's installed

| Piece | Location | Notes |
| --- | --- | --- |
| Python package | `.headroom-venv/` | `headroom-ai[mcp,proxy]` in an isolated venv (Ubuntu's system Python is PEP-668 externally-managed). Not committed; rebuildable (see below). |
| MCP registration | `.mcp.json` (gitignored) | Runs `<venv>/bin/headroom mcp serve` over stdio. Copy from [`.mcp.json.example`](../.mcp.json.example) and fix the path — not committed live, since it points at the uncommitted venv and would break any fresh/cloud clone. |
| Tool approvals | `.claude/settings.local.json` | The three `mcp__headroom__*` tools are pre-allowed so they don't prompt per call. |
| Proxy routing | `.claude/settings.local.json` | `env.ANTHROPIC_BASE_URL` pins this project's Claude Code at the local proxy, plus a `SessionStart` hook that starts it. Machine-local on purpose — see [Always-on proxy](#always-on-proxy). |
| Proxy service | `~/.config/systemd/user/headroom-proxy.service` → `~/.local/bin/headroom-proxy-launch` | Shared machine-wide, `Restart=always`. Not owned by this project. |
| Proxy starter | [`scripts/headroom_ensure.sh`](../scripts/headroom_ensure.sh) | Idempotent up-check used by the `SessionStart` hook. |
| Test | [`headroom-test.sh`](../headroom-test.sh) → [`tools/headroom_compression_test.py`](../tools/headroom_compression_test.py) | End-to-end check of compress + retrieve + stats. |

## Using it in Claude Code

A newly-added MCP server is only picked up on startup. **Restart Claude Code**;
the first time it loads you'll get a one-time prompt to trust the `headroom`
server from `.mcp.json`. After that, three tools are available:

- `mcp__headroom__headroom_compress` - shrink a large blob; returns the
  compressed text plus a retrieval `hash`.
- `mcp__headroom__headroom_retrieve` - fetch the full original back by `hash`
  (optionally filtered by a query).
- `mcp__headroom__headroom_stats` - session compression / token-savings stats.

The on-demand tools use a **local store - no proxy or API key required**.

Note the tools are *opt-in*: nothing is compressed unless Claude explicitly hands
a blob to `headroom_compress`, and the router declines small payloads
(`router:noop`) and anything containing error/warning lines
(`router:protected:error_output`), returning them verbatim. For automatic
compression of every request, see below.

## Always-on proxy

This project routes **all** its Claude Code traffic through the local proxy, so
large tool output is compressed inline without anyone having to ask for it.

Three pieces, all machine-local:

1. `env.ANTHROPIC_BASE_URL` in `.claude/settings.local.json` points Claude Code
   at `http://127.0.0.1:8787`.
2. `headroom-proxy.service` (systemd `--user`) runs the proxy with
   `Restart=always` in `--mode cache`, which freezes prior turns so Anthropic's
   prefix cache still hits.
3. A `SessionStart` hook runs [`scripts/headroom_ensure.sh`](../scripts/headroom_ensure.sh),
   which is a no-op (~30ms) when the proxy is already up and cold-starts it
   (~3s) when it isn't. It merges with — does not replace — the existing
   `cloud_setup.sh` SessionStart hook in the committed `settings.json`.

**One proxy, shared.** The proxy is a stateless localhost forwarder, so a single
instance serves every project that routes through it; the Medical Game project
uses the same one. The service therefore doesn't point at this repo's venv
directly — `~/.local/bin/headroom-proxy-launch` picks whichever project venv is
present, so deleting either checkout doesn't break the other.

**Why `settings.local.json` and not the committed `settings.json`:** the venv
isn't committed, so on any other machine (or a cloud session) the base URL would
point at a dead port and Claude Code would fail every request. This has to stay
personal config.

Enable the service at login (one-off):

```bash
systemctl --user enable headroom-proxy.service
```

### If it breaks

Because the base URL is pinned, a dead proxy means **no API access in this
project**. The `SessionStart` hook warns loudly if the proxy won't come up. To
bypass entirely, delete the `env` block from `.claude/settings.local.json`.

```bash
systemctl --user status headroom-proxy.service   # is it alive?
./.headroom-venv/bin/headroom doctor             # end-to-end wiring check
./.headroom-venv/bin/headroom savings            # what it's actually saved
```

`doctor`'s `claude: not routed` warning is a **false negative here** — it only
reads `~/.claude/settings.json` and can't see project-scoped settings. Trust the
`shell env` row instead.

## Testing

```bash
./headroom-test.sh
```

Drives the real MCP stdio server the same way Claude Code does and asserts the
tools exist, that a verbose JSON payload compresses by ≥30% (typically ~40–60%),
that retrieve round-trips the *exact* original, and that stats update. Exits
non-zero with a one-line diagnostic on failure.

## Maintenance

- **Rebuild the venv** (e.g. after deleting it or on a new machine):
  ```bash
  python3 -m venv .headroom-venv
  ./.headroom-venv/bin/pip install 'headroom-ai[mcp,proxy]'
  ```
- **Upgrade:** `./.headroom-venv/bin/pip install -U 'headroom-ai[mcp,proxy]'`
- **CLI help:** `./.headroom-venv/bin/headroom mcp --help`

## Gotcha

`headroom_stats` changes output shape depending on whether a proxy is reachable:
a JSON object when there's none, a human-readable report when there is. The test
accepts both — anything else parsing that tool must too.

A manual newline-delimited JSON-RPC pipe (`echo '{...}' | headroom mcp serve`)
makes `headroom_compress` *look* like it hangs - that's a stdin-EOF race where
the async server tears down before flushing the response, **not** a bug. Always
test with a real MCP stdio client (as the test does).
