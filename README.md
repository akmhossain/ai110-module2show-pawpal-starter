# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan


## What you will build

The final app does the following:

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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
========================================
TODAY'S SCHEDULE
========================================
Schedule for 2026-06-29 (Alex):
  - [HIGH] Morning Walk (30 min) [7:15am] — Buddy
  - [HIGH] Feed Breakfast (10 min) [8:00am] — Buddy
  - [HIGH] Feed Dinner (10 min) [5:00pm] — Luna
  - [MEDIUM] Clean Litter Box (15 min) [9:30am] — Luna
  - [MEDIUM] Evening Walk (25 min) [6:00pm] — Buddy
  - [LOW] Evening Playtime (20 min) [6:45pm] — Luna
Total: 110 / 120 min

========================================
SORTED BY TIME
========================================
      7:15am  [ HIGH ]  Morning Walk (Buddy)
      8:00am  [ HIGH ]  Feed Breakfast (Buddy)
      9:30am  [MEDIUM]  Clean Litter Box (Luna)
      5:00pm  [ HIGH ]  Feed Dinner (Luna)
      6:00pm  [MEDIUM]  Evening Walk (Buddy)
      6:45pm  [ LOW  ]  Evening Playtime (Luna)

========================================
FILTER: Buddy's tasks only
========================================
  Morning Walk — high
  Feed Breakfast — high
  Evening Walk — medium

========================================
FILTER: Incomplete tasks only
========================================
  Morning Walk (Buddy) — done=False
  Feed Breakfast (Buddy) — done=False
  Evening Walk (Buddy) — done=False
  Clean Litter Box (Luna) — done=False
  Evening Playtime (Luna) — done=False

========================================
FILTER: Completed tasks only
========================================
  Feed Dinner (Luna) — done=True

========================================
CONFLICT DETECTION TEST
========================================
WARNING: 'Feed Breakfast' (Buddy) and 'Brush Teeth' (Buddy) are both scheduled at 8:00am.
WARNING: 'Feed Breakfast' (Buddy) and 'Morning Meds' (Luna) are both scheduled at 8:00am.
WARNING: 'Brush Teeth' (Buddy) and 'Morning Meds' (Luna) are both scheduled at 8:00am.
```

## 🧪 Testing PawPal+

### Test Descriptions:
Tests include checking if a tasks is properly marked true, if a pet's task count increases properly, if a schedule is properly sorted chronlogically (both by time and string), if a recurring task is properly made and added, if a non-recurring task produces no task, and if conflicts are properly detected or no conflict. 

Confidence level: 4/5 stars because tests ensure that functions work properly in multiple scenarios, whether something is added or not. However, without actually using the app we won't truly test to its limits.

How to run:

```bash
# Mac version:
python3 -m pytest
```

Sample test output:

```
tests/test_pawpal.py .............                                       [100%]

============================== 13 passed in 0.02s ==============================
Finished running tests!
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sort by priority + time | `Scheduler.sort_tasks()` | Sorts by priority (high → low), then by `preferred_time` as a tiebreaker |
| Sort by time only | `Scheduler.sort_by_time()` | Chronological order using `get_time_minutes()`; tasks with no time go last |
| Filtering | `Scheduler.filter_tasks()` | Filter by priority, pet name, preferred time, time window (after/before), or completion status |
| Conflict detection | `Scheduler.detect_conflicts()` | Pairwise check for tasks sharing the same `preferred_time`; returns warning strings without crashing |
| Recurring tasks | `Task.mark_complete()` / `Scheduler.complete_task()` | Daily tasks reschedule +1 day; weekly tasks reschedule +7 days using `timedelta` |
| Budget enforcement | `Scheduler.generate_plan()` / `is_within_budget()` | Tasks are selected in priority order until the owner's `available_minutes` is exhausted |

## 📸 Demo Walkthrough

### Main UI features

- **Owner & Pet Setup** — Enter the owner's name and daily available minutes, then add one or more pets (name, species, breed, age). Each new pet is attached to the current owner.
- **Tasks** — Once at least one pet exists, add care tasks by choosing the pet, a task title, duration, priority (low/medium/high), and a preferred time slot. Added tasks are checked against existing tasks for scheduling conflicts and shown in a running table.
- **Build Schedule** — Generates a daily plan by calling `Scheduler.generate_plan()`, which selects tasks in priority order until the owner's available time budget is used up. Shows the resulting schedule, any conflict warnings, a text explanation of the plan (`explain_plan()`), and a toggle to view the schedule sorted by priority or by time. Tasks that didn't fit in the time budget are listed separately as "Skipped."
- **Filter Scheduled Tasks** — After a schedule is generated, filter the scheduled tasks by priority, time window (morning/afternoon/evening), and/or pet name to quickly find specific tasks.

### Example workflow

1. Enter owner info ("Jordan", 120 available minutes) and add a pet ("Mochi", a dog) — click **Add pet**.
2. Add a task for Mochi, e.g. "Morning walk," 30 minutes, high priority, 7:00am — click **Add task**. Repeat for a few more tasks across priorities and times.
3. Click **Generate schedule** to build today's plan. The app fills the schedule in priority order until the time budget runs out, showing which tasks made it in and which were skipped.
4. Toggle between "sort by priority" and "sort by time" to see the same schedule reorganized.
5. Use the filter controls to narrow the scheduled tasks down to, say, only "high" priority tasks or only tasks for one pet.

### Key Scheduler behaviors shown

- **Sorting** — `sort_tasks()` orders tasks by priority (high → low) with preferred time as a tiebreaker; `sort_by_time()` instead orders purely chronologically, pushing tasks with no preferred time to the end.
- **Conflict warnings** — `detect_conflicts()` flags any tasks sharing the same preferred time slot as warnings (e.g. two tasks both set for 7:00am), without blocking the user from adding them.
- **Budget enforcement** — `generate_plan()` fills the schedule in priority order and stops once the owner's `available_minutes` is exhausted, moving any leftover tasks to the "Skipped" list.
- **Recurring tasks** — completing a daily task reschedules it +1 day, and a weekly task reschedules +7 days, via `Task.mark_complete()` / `Scheduler.complete_task()`.


## System Architecture

UML diagram that outlines how objects interact with each other

![UML diagram](image.png)
