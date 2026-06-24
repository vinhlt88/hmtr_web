# Workspace Rules for Agents

- **Tournament Scheduling**: Whenever the user asks to schedule a football or sports tournament (especially with constraints like weekends, specific timeslots, rest days, or asymmetric group sizes), you MUST use the `tournament_scheduler` skill. Do not write a simple greedy algorithm or a standard round-robin generator. Read the `SKILL.md` inside `.agents/skills/tournament_scheduler/` and heavily refer to `examples/z3_reference.py` for the Z3 mathematical solver template.
