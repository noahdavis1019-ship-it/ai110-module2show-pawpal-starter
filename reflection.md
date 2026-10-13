# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I started with four classes. Task holds a single activity (description, time,
frequency, completion flag). Pet holds its name, species, and a list of its own
Tasks. Owner holds a name and a list of Pets. Scheduler is the brain that reads
across the Owner to sort, filter, and report on all tasks. Three core user actions
drove the design: add a pet, schedule a task, and view today's schedule.

**b. Design changes**

The biggest change was how the Scheduler returns data. My first skeleton had it
returning plain Task objects, but once I tried to print a schedule I realized I
also needed to know which pet each task belonged to. I changed `Owner.all_tasks()`
and the Scheduler methods to work with `(pet, task)` pairs instead of bare tasks.
I also added a `due_date` field to Task during Phase 4 so recurrence had a real
date to advance with `timedelta`.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers task time (for chronological ordering), pet and completion
status (for filtering), frequency (for recurrence), and time collisions (for
conflict detection). Time mattered most because a daily plan is only useful if a
pet owner can read it in the order the day actually happens.

**b. Tradeoffs**

Conflict detection only flags exact time matches, not overlapping durations. A
30-minute walk at 08:00 and a feeding at 08:15 would not be flagged even though
they overlap. That is reasonable here because tasks are stored as a single `HH:MM`
start time with no duration, so exact-match is the honest limit of the data I have,
and it keeps the check simple and fast rather than guessing at overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

I used an AI coding assistant to brainstorm the Mermaid UML, scaffold the class
skeletons from that diagram, and draft the pytest cases. The most helpful prompts
were specific ones that referenced my actual files, like asking how the Scheduler
should retrieve tasks from the Owner's pets given my skeletons, rather than generic
"write me a scheduler" prompts.

**b. Judgment and verification**

One suggestion I modified: the assistant proposed storing tasks in a single global
list on the Scheduler. I rejected that because it broke the "Pet owns its tasks"
relationship from my UML and would have made `task_count()` per pet awkward. I kept
tasks on each Pet and had the Scheduler read across them instead. I verified every
behavior by running `python main.py` and `python -m pytest` after each change
rather than trusting the generated code on sight.

---

## 4. Testing and Verification

**a. What you tested**

I tested status flips on completion, task counts, chronological sorting, filtering
by pet and status, daily recurrence creating a next-day task, one-off tasks not
recurring, exact-time conflict detection, and the empty-owner edge case. These
cover both the OOP basics and all four algorithms, so a regression in any feature
shows up as a failing test.

**b. Confidence**

I am confident (4 of 5 stars) the scheduler works for the behaviors it claims.
With more time I would test overlapping-duration conflicts, invalid time strings,
and weekly recurrence landing on the correct day across a month boundary.

---

## 5. Reflection

**a. What went well**

The CLI-first workflow. Getting `main.py` printing a clean, sorted schedule before
touching Streamlit meant the UI work in `app.py` was mostly wiring, not debugging
logic and layout at the same time.

**b. What you would improve**

I would give Task a real duration and make conflict detection check for overlap
rather than exact start-time collisions. I would also persist the schedule to disk
so it survives closing the app.

**c. Key takeaway**

Being the lead architect meant the AI was fastest at producing code but I had to
own the structure. Keeping my UML as the source of truth let me catch suggestions
that were clever but off-design, and verifying with tests after every step kept the
generated code honest.
