import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(task_id="t1", name="Walk", category="exercise", duration_minutes=20, priority="high")
    assert task.is_completed is False
    task.mark_complete()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
    assert len(pet.tasks) == 0
    task = Task(task_id="t2", name="Feed", category="feeding", duration_minutes=10, priority="medium")
    pet.add_task(task)
    assert len(pet.tasks) == 1


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_task(task_id="t1", name="Task", priority="medium", duration=10,
              preferred_time=None, recurrence=None, is_recurring=False, due_date=None):
    return Task(
        task_id=task_id,
        name=name,
        category="general",
        duration_minutes=duration,
        priority=priority,
        preferred_time=preferred_time,
        recurrence=recurrence,
        is_recurring=is_recurring,
        due_date=due_date,
    )


def make_scheduler(tasks=None, available_minutes=240):
    owner = Owner(name="Alex", available_minutes=available_minutes)
    s = Scheduler(date="2026-07-02", owner=owner)
    for t in (tasks or []):
        s.add_task(t)
    return s


# ===========================================================================
# SORTING CORRECTNESS — tasks returned in chronological order
# ===========================================================================

def test_sort_by_time_chronological_order():
    """Tasks with explicit times should come back earliest-first."""
    evening = make_task("c", "Evening Walk", preferred_time="evening")   # 18:00 → 1080 min
    morning = make_task("a", "Morning Feed", preferred_time="morning")   # 07:00 → 420 min
    afternoon = make_task("b", "Afternoon Play", preferred_time="afternoon")  # 13:00 → 780 min

    s = make_scheduler([evening, morning, afternoon])
    result = s.sort_by_time()

    assert [t.task_id for t in result] == ["a", "b", "c"]


def test_sort_by_time_clock_strings_chronological():
    """Clock-string preferred_times should also sort chronologically."""
    t1 = make_task("a", "Early", preferred_time="8:00am")   # 480 min
    t2 = make_task("b", "Mid", preferred_time="10:30am")    # 630 min
    t3 = make_task("c", "Late", preferred_time="2:00pm")    # 840 min

    s = make_scheduler([t3, t1, t2])
    result = s.sort_by_time()

    assert [t.task_id for t in result] == ["a", "b", "c"]


def test_sort_by_time_untimed_tasks_go_to_end():
    """Tasks with no preferred_time should appear after all timed tasks."""
    timed = make_task("a", "Morning Walk", preferred_time="morning")
    untimed = make_task("b", "Untimed Grooming")

    s = make_scheduler([untimed, timed])
    result = s.sort_by_time()

    assert result[0].task_id == "a"
    assert result[1].task_id == "b"


# ===========================================================================
# RECURRENCE LOGIC — daily task completion creates next-day task
# ===========================================================================

def test_daily_recurrence_creates_next_day_task():
    """Completing a daily task should produce a new task due the following day."""
    t = make_task("feed1", "Morning Feed", recurrence="daily",
                  is_recurring=True, due_date=date(2026, 7, 2))

    next_task = t.mark_complete()

    assert next_task is not None
    assert next_task.due_date == date(2026, 7, 3)


def test_daily_recurrence_next_task_added_to_schedule():
    """complete_task() should append the next occurrence to the scheduler's task list."""
    t = make_task("feed1", "Morning Feed", recurrence="daily",
                  is_recurring=True, due_date=date(2026, 7, 2))
    s = make_scheduler([t])

    s.complete_task("feed1")

    assert len(s.tasks) == 2
    assert s.tasks[-1].due_date == date(2026, 7, 3)


def test_non_recurring_task_produces_no_next_task():
    """Completing a non-recurring task should return None with no new tasks added."""
    t = make_task("bath1", "Bath Time", recurrence=None)
    s = make_scheduler([t])

    result = s.complete_task("bath1")

    assert result is None
    assert len(s.tasks) == 1


# ===========================================================================
# CONFLICT DETECTION — scheduler flags duplicate times
# ===========================================================================

def test_conflict_detected_for_same_named_period():
    """Two tasks at the same named period should trigger a warning."""
    t1 = make_task("a", "Walk", preferred_time="morning")
    t2 = make_task("b", "Feed", preferred_time="morning")
    s = make_scheduler([t1, t2])

    warnings = s.detect_conflicts()

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feed" in warnings[0]


def test_conflict_detected_for_same_clock_time():
    """Two tasks at identical clock strings should be flagged."""
    t1 = make_task("a", "Medication", preferred_time="8:00am")
    t2 = make_task("b", "Breakfast", preferred_time="8:00am")
    s = make_scheduler([t1, t2])

    warnings = s.detect_conflicts()

    assert len(warnings) == 1


def test_no_conflict_for_different_times():
    """Tasks at different times should produce no warnings."""
    t1 = make_task("a", "Walk", preferred_time="morning")
    t2 = make_task("b", "Feed", preferred_time="evening")
    s = make_scheduler([t1, t2])

    assert s.detect_conflicts() == []


def test_no_conflict_when_no_times_set():
    """Tasks without preferred_time should never conflict."""
    t1 = make_task("a", "Walk")
    t2 = make_task("b", "Feed")
    s = make_scheduler([t1, t2])

    assert s.detect_conflicts() == []


def test_conflict_warning_names_both_tasks():
    """The warning message should identify both conflicting task names."""
    t1 = make_task("a", "Grooming", preferred_time="afternoon")
    t2 = make_task("b", "Vet Call", preferred_time="afternoon")
    s = make_scheduler([t1, t2])

    warning = s.detect_conflicts()[0]

    assert "Grooming" in warning
    assert "Vet Call" in warning
