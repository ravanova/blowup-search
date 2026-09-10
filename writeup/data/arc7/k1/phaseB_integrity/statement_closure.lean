import NavierStokes.ComparatorSolution
open Lean

/-- Semantic closure of a STATEMENT. Follow: the type of every constant; the VALUE of
    definitions (a def's meaning includes its body); and, for an inductive/structure,
    its CONSTRUCTORS (that is where the fields live). Theorem PROOF bodies are not
    followed: they are irrelevant to meaning and are separately kernel-checked. -/
partial def go (env : Environment) : List Name → NameSet → NameSet
  | [], acc => acc
  | n :: rest, acc =>
    if acc.contains n then go env rest acc
    else
      let acc := acc.insert n
      match env.find? n with
      | none => go env rest acc
      | some ci =>
        let fromType := ci.type.getUsedConstants.toList
        let extra :=
          match ci with
          | .thmInfo _ => []
          | .inductInfo iv => iv.ctors ++ iv.all
          | _ => match ci.value? with
                 | some v => v.getUsedConstants.toList
                 | none => []
        go env (fromType ++ extra ++ rest) acc

def roots : List Name :=
  [`NavierStokes.Comparator.navier_stokes_breakdown_R3,
   `NavierStokes.Comparator.navier_stokes_breakdown_periodic]

def main : IO Unit := do
  let env ← importModules #[{module := `NavierStokes.ComparatorSolution}] {} 0
  let cl := go env roots {}
  let names := cl.toList
  let mut mods : Std.HashMap Name Nat := {}
  for n in names do
    if let some idx := env.getModuleIdxFor? n then
      mods := mods.insert (env.header.moduleNames[idx.toNat]!) 1
  let mathlibMods := mods.toList.filter (fun (m, _) => (`Mathlib).isPrefixOf m)
  IO.println s!"statement_closure_constants = {names.length}"
  IO.println s!"modules_total = {mods.size}"
  IO.println s!"MATHLIB modules in statement closure = {mathlibMods.length}  (of 8370 mathlib source files)"
  IO.println s!"project modules = {(mods.toList.filter (fun (m,_) => (`NavierStokes).isPrefixOf m)).length}"
  IO.println "-- mathlib modules in the statement closure (sorted):"
  for (m, _) in (mathlibMods.toArray.qsort (fun a b => a.1.lt b.1)).toList do
    IO.println s!"  {m}"
