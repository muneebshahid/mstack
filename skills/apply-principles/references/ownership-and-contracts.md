# Ownership and Contracts

## Clear ownership

Give each invariant and its mutations, effects, lifecycle, and failure policy an obvious owner. Keep responsibilities together when they share invariants and change for the same reason; separate them when their policies or lifecycles differ. Put behavior beside the concept that owns it instead of forwarding through managers or hiding it in generic utilities.

## Boundary discipline

Validate external and untrusted input where it enters, including persisted, cached, and deserialized data. Parse into domain values once, then rely on the guarantees their construction establishes.

Make inputs, outputs, effects, failures, and compatibility explicit where ambiguity creates risk. Keep storage and transport representations private; translate mechanism-specific errors into the application's contract. Do not turn invalid input or failed checks into successful defaults that bypass required validation. Avoid repeating established checks inside business logic.

## Dependency direction

Keep stable policy independent of volatile frameworks and infrastructure. Runtime calls may flow outward to mechanisms while source dependencies point inward toward policy. At a real architectural seam, define a narrow contract and connect its implementation through an adapter or composition root. Do not hide a dependency cycle behind dynamic lookup or add interfaces solely to satisfy a pattern.
