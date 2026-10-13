# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule for Noah
  08:00  Morning walk (Biscuit) [daily] [todo]
  08:00  Feed (Mochi) [daily] [todo]
  14:30  Vet appointment (Mochi) [once] [todo]
  18:00  Evening walk (Biscuit) [daily] [todo]

Only Mochi's tasks:
  08:00  Feed (Mochi) [daily] [todo]
  14:30  Vet appointment (Mochi) [once] [todo]
```

## 🧪 Testing PawPal+

Run the full suite with:

```bash
python -m pytest
```

The suite covers status flips, task counts, chronological sorting, pet/status
filtering, daily recurrence on completion, one-off tasks not recurring, same-time
conflict detection, and empty-owner edge cases.

Sample test output:

```
============================= test session starts ==============================
platform linux -- Python 3.13.16, pytest-9.1.1, pluggy-1.6.0
collected 9 items

tests/test_pawpal.py .........                                           [100%]

============================== 9 passed in 0.03s ===============================
```

**Confidence Level: ★★★★☆** — Core logic and all four algorithms are covered by
passing tests. Dropped one star because conflicts are detected only on exact time
matches, not overlapping durations.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` / `todays_schedule()` | Sorts (pet, task) pairs by the task's `HH:MM` string |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Filter by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Returns warning strings for tasks sharing a time slot |
| Recurring tasks | `Task.next_occurrence()` + `Scheduler.complete_task()` | Completing a daily/weekly task spawns the next occurrence via `timedelta` |

## 📸 Demo Walkthrough

Run the app with `streamlit run app.py`. The owner is held in `st.session_state`
so pets and tasks persist across reruns.

**Main features**
- Add pets (name + species) through a form.
- Add tasks to any pet with a time (`HH:MM`) and frequency (once/daily/weekly).
- View a time-sorted schedule in a table.
- See conflict warnings when two tasks share a time slot.
- Complete a task; daily/weekly ones automatically reschedule for the next occurrence.

**Example workflow**
1. Add a pet named Biscuit (dog).
2. Add "Morning walk" at 08:00, daily.
3. Add a second pet Mochi (cat) and a "Feed" task at 08:00, daily.
4. The schedule table lists both at 08:00 and a warning flags the 08:00 conflict.
5. Mark "Morning walk" complete; a new Morning walk appears for tomorrow.

**Key Scheduler behaviors shown:** chronological sorting, exact-time conflict
warnings, and daily/weekly recurrence.

Sample CLI output from `python main.py`:

```
Today's Schedule for Noah
  08:00  Morning walk (Biscuit) [daily] [todo]
  08:00  Feed (Mochi) [daily] [todo]
  14:30  Vet appointment (Mochi) [once] [todo]
  18:00  Evening walk (Biscuit) [daily] [todo]

Conflict check:
  ! Conflict at 08:00: Morning walk (Biscuit) and Feed (Mochi)

Complete Biscuit's morning walk (daily) -> rolls to tomorrow:
  next occurrence due 2026-10-14 at 08:00
```
