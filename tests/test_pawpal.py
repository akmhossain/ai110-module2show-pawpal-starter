import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


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
