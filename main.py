from pawpal_system import Task, Pet, Owner, Scheduler

# Owner
owner = Owner(name="Alex", available_minutes=120)

# Pets
dog = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
cat = Pet(name="Luna", species="Cat", breed="Siamese", age=5)

# Tasks for Buddy
dog.add_task(Task(task_id="t1", name="Morning Walk", category="exercise", duration_minutes=30, priority="high", preferred_time="7:15am"))
dog.add_task(Task(task_id="t2", name="Feed Breakfast", category="feeding", duration_minutes=10, priority="high", preferred_time="8:00am"))

# Tasks for Luna
cat.add_task(Task(task_id="t3", name="Clean Litter Box", category="hygiene", duration_minutes=15, priority="medium", preferred_time="9:30am"))
cat.add_task(Task(task_id="t4", name="Evening Playtime", category="enrichment", duration_minutes=20, priority="low", preferred_time="6:45pm"))

# Register pets with owner
owner.add_pet(dog)
owner.add_pet(cat)

# Build schedule
schedule = Scheduler(date="2026-06-28", owner=owner)
schedule.generate_plan()

print("=" * 40)
print("TODAY'S SCHEDULE")
print("=" * 40)
print(schedule.explain_plan())
