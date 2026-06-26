from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    task_id: str
    name: str
    category: str
    duration_minutes: int
    priority: str  # "high", "medium", "low"
    is_recurring: bool = False
    preferred_time: Optional[str] = None  # e.g., "morning", "evening"
    notes: str = ""

    def is_high_priority(self) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    special_needs: list[str] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_special_need(self, need: str) -> None:
        pass

    def get_profile(self) -> dict:
        pass

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def get_available_times(self) -> int:
        pass

    def add_available_times(self, minutes: int) -> int:
        pass

    def set_preferences(self, prefs: dict) -> None:
        pass

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Schedule:
    date: str
    owner: Owner
    pet: Pet
    tasks: list[Task] = field(default_factory=list)

    def generate_plan(self) -> None:
        pass

    def sort_tasks(self) -> list[Task]:
        pass

    def filter_tasks(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def get_total_duration(self) -> int:
        pass

    def is_within_budget(self) -> bool:
        pass
