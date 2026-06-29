from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional
import re


@dataclass
class Task:
    task_id: str
    name: str
    category: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    pet_name: str = ""  # name of the pet this task belongs to
    is_completed: bool = False
    is_recurring: bool = False
    recurrence: Optional[str] = None  # "daily" or "weekly"
    due_date: Optional[date] = None
    preferred_time: Optional[str] = None  # e.g., "morning", "evening"
    notes: str = ""

    def is_high_priority(self) -> bool:
        """Return True if this task's priority is high."""
        return self.priority == "high"

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and return the next occurrence for recurring tasks.

        Sets is_completed to True. If recurrence is 'daily' or 'weekly', calculates
        the next due_date using timedelta (days=1 or weeks=1) relative to the task's
        existing due_date, falling back to today if none is set. Returns a new Task
        with the same fields and the updated due_date, or None for non-recurring tasks.
        """
        self.is_completed = True
        if self.recurrence == "daily":
            delta = timedelta(days=1)
        elif self.recurrence == "weekly":
            delta = timedelta(weeks=1)
        else:
            return None
        base = self.due_date if self.due_date else date.today()
        return Task(
            task_id=f"{self.task_id}_next",
            name=self.name,
            category=self.category,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            pet_name=self.pet_name,
            is_recurring=self.is_recurring,
            recurrence=self.recurrence,
            due_date=base + delta,
            preferred_time=self.preferred_time,
            notes=self.notes,
        )

    def get_time_minutes(self) -> Optional[int]:
        """Convert preferred_time (named period or clock string) to minutes from midnight."""
        if not self.preferred_time:
            return None
        t = self.preferred_time.strip().lower()
        named = {"morning": 7 * 60, "afternoon": 13 * 60, "evening": 18 * 60, "night": 21 * 60}
        if t in named:
            return named[t]
        match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?(am|pm)", t)
        if match:
            hour, minute, period = match.groups()
            hour, minute = int(hour), int(minute or 0)
            if period == "pm" and hour != 12:
                hour += 12
            elif period == "am" and hour == 12:
                hour = 0
            return hour * 60 + minute
        return None


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_special_need(self, need: str) -> None:
        """Add a special need to this pet if it isn't already listed."""
        if need not in self.special_needs:
            self.special_needs.append(need)

    def get_profile(self) -> dict:
        """Return a summary dict of this pet's attributes and task count."""
        return {
            "name": self.name,
            "species": self.species,
            "breed": self.breed,
            "age": self.age,
            "special_needs": self.special_needs,
            "task_count": len(self.tasks),
        }

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and set the task's pet_name."""
        task.pet_name = self.name
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def get_available_times(self) -> int:
        """Return the owner's total available minutes for the day."""
        return self.available_minutes

    def add_available_times(self, minutes: int) -> None:
        """Increase the owner's available minutes by the given amount."""
        self.available_minutes += minutes

    def set_preferences(self, prefs: dict) -> None:
        """Merge the given preferences into the owner's preferences dict."""
        self.preferences.update(prefs)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner if not already added."""
        if pet not in self.pets:
            self.pets.append(pet)


@dataclass
class Scheduler:
    date: str
    owner: Owner
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task directly to this schedule."""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove the task with the given ID from the schedule."""
        self.tasks = [t for t in self.tasks if t.task_id != task_id]

    def get_total_duration(self) -> int:
        """Return the sum of all scheduled task durations in minutes."""
        return sum(t.duration_minutes for t in self.tasks)

    def is_within_budget(self) -> bool:
        """Return True if total task duration fits within the owner's available minutes."""
        return self.get_total_duration() <= self.owner.available_minutes

    def sort_tasks(self) -> list[Task]:
        """Return tasks sorted by priority then by time of day."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.tasks,
            key=lambda t: (priority_order.get(t.priority, 3), t.get_time_minutes() or 0),
        )

    def complete_task(self, task_id: str) -> Optional[Task]:
        """Mark a task complete by ID and automatically schedule its next occurrence.

        Finds the task with the given task_id, calls mark_complete() on it, and
        appends the returned next Task to the schedule if one is produced (i.e. the
        task has a 'daily' or 'weekly' recurrence). Returns the new Task, or None
        if the task_id was not found or the task is not recurring.
        """
        for task in self.tasks:
            if task.task_id == task_id:
                next_task = task.mark_complete()
                if next_task:
                    self.tasks.append(next_task)
                return next_task
        return None

    def detect_conflicts(self) -> list[str]:
        """Return warning messages for any tasks that share the same scheduled time.

        Compares all tasks that have a preferred_time set using get_time_minutes().
        For every pair of tasks whose resolved minute values are equal, appends a
        human-readable warning string naming both tasks and their common time.
        Tasks without a preferred_time are ignored. Returns an empty list if no
        conflicts exist. Does not raise exceptions or modify the schedule.
        """
        warnings = []
        timed = [t for t in self.tasks if t.get_time_minutes() is not None]
        for i, a in enumerate(timed):
            for b in timed[i + 1:]:
                if a.get_time_minutes() == b.get_time_minutes():
                    warnings.append(
                        f"WARNING: '{a.name}' ({a.pet_name or 'unknown'}) and "
                        f"'{b.name}' ({b.pet_name or 'unknown'}) are both scheduled at {a.preferred_time}."
                    )
        return warnings

    def sort_by_time(self) -> list[Task]:
        """Return tasks sorted chronologically by preferred_time.

        Uses get_time_minutes() to convert each task's preferred_time to minutes
        from midnight, enabling consistent comparison across named periods (e.g.
        'morning') and clock strings (e.g. '8:00am'). Tasks with no preferred_time
        are sorted to the end. Does not modify self.tasks in place.
        """
        return sorted(
            self.tasks,
            key=lambda t: (t.get_time_minutes() is None, t.get_time_minutes() or 0),
        )

    def filter_tasks(
        self,
        priority: Optional[str] = None,
        preferred_time: Optional[str] = None,
        pet_name: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
        is_completed: Optional[bool] = None,
    ) -> list[Task]:
        """Filter tasks by priority, time period/exact time, pet name, completion
        status, or a time window defined by after/before (e.g. after='8:00am', before='12:00pm')."""
        result = self.tasks
        if priority:
            result = [t for t in result if t.priority == priority]
        if preferred_time:
            result = [t for t in result if t.preferred_time == preferred_time]
        if pet_name:
            result = [t for t in result if t.pet_name == pet_name]
        if is_completed is not None:
            result = [t for t in result if t.is_completed == is_completed]
        if after:
            after_min = Task("", "", "", 0, "", preferred_time=after).get_time_minutes()
            if after_min is not None:
                result = [t for t in result if (t.get_time_minutes() or 0) >= after_min]
        if before:
            before_min = Task("", "", "", 0, "", preferred_time=before).get_time_minutes()
            if before_min is not None:
                result = [t for t in result if (t.get_time_minutes() or 0) <= before_min]
        return result

    def generate_plan(self) -> list[Task]:
        """Build the schedule by fitting the owner's pets' tasks within the available time budget."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)

        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_tasks = sorted(all_tasks, key=lambda t: priority_order.get(t.priority, 3))

        budget = self.owner.available_minutes
        self.tasks = []
        for task in sorted_tasks:
            if task.duration_minutes <= budget:
                self.tasks.append(task)
                budget -= task.duration_minutes

        return self.tasks

    def explain_plan(self) -> str:
        """Return a readable summary of the scheduled tasks and total time used."""
        if not self.tasks:
            return "No tasks scheduled."

        lines = [f"Schedule for {self.date} ({self.owner.name}):"]
        for task in self.sort_tasks():
            time_note = f" [{task.preferred_time}]" if task.preferred_time else ""
            lines.append(
                f"  - [{task.priority.upper()}] {task.name} ({task.duration_minutes} min){time_note}"
                + (f" — {task.pet_name}" if task.pet_name else "")
            )
        lines.append(f"Total: {self.get_total_duration()} / {self.owner.available_minutes} min")
        return "\n".join(lines)
