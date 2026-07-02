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

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
========================================
TODAY'S SCHEDULE
========================================
Schedule for 2026-06-28 (Alex):
  - [HIGH] Morning Walk (30 min) [7:15am] — Buddy
  - [HIGH] Feed Breakfast (10 min) [8:00am] — Buddy
  - [MEDIUM] Clean Litter Box (15 min) [9:30am] — Luna
  - [LOW] Evening Playtime (20 min) [6:45pm] — Luna
Total: 75 / 120 min
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

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
