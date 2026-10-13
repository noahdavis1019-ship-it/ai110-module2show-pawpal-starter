# AI Interactions Log

> Stretch feature documentation for PawPal+.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to take my Phase 1 UML skeleton in `pawpal_system.py` and
implement the recurring-task feature end to end: a daily or weekly task, when
marked complete, should automatically create its next occurrence, and the
Scheduler should handle the hand-off so the new task lands on the right pet.

**What did the agent do?**

- Added a `due_date` field to the `Task` dataclass (defaulting to today) so
  recurrence had a real date to advance.
- Wrote `Task.next_occurrence()` using `datetime.timedelta` to add 1 day for
  daily and 1 week for weekly, returning `None` for one-off tasks.
- Added `Scheduler.complete_task(pet, task)` to mark the task complete and append
  the next occurrence to that pet.
- Updated `main.py` to demonstrate completing a daily task and printing the next
  due date.
- Added tests for daily recurrence, one-off non-recurrence, and the next-day due
  date.

**What did you have to verify or fix manually?**

The agent's first version put the recurrence logic entirely inside
`Task.mark_complete()`, which meant the Task tried to append a new task to a pet
it had no reference to. I moved the "create next occurrence" step up into
`Scheduler.complete_task()` so the Pet that owns the task does the appending,
keeping Task ignorant of Pet. I verified the fix by running `python -m pytest`
and confirming the next-day due date with `main.py`.

---

## Prompt Comparison (SF11)

> Compare two different prompts on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | Claude (agent mode) | Claude (plain chat) |
| **Prompt** | "Based on my skeletons in pawpal_system.py, implement conflict detection that returns warnings instead of crashing." | "Write a function to find scheduling conflicts in a list of tasks." |
| **Response summary** | Read my actual classes and returned a `Scheduler.detect_conflicts()` method that walks sorted (pet, task) pairs and builds warning strings. | Returned a generic standalone function assuming a flat list of dicts with `start`/`end` fields I did not have. |
| **What was useful** | Matched my data model and integrated directly. | The nested-loop comparison idea was sound. |
| **Problems noticed** | Slightly verbose. | Assumed task durations and a data shape my system doesn't use. |
| **Decision** | Used Option A. | Rejected; would have required rewriting my Task class. |

**Which approach did you use in your final implementation and why?**

I used Option A. Giving the agent my real file meant its output fit my
`(pet, task)` structure instead of forcing my design to match a generic snippet.
The main lesson: prompts that reference your actual code beat generic
"write me X" prompts because the result drops straight in.
