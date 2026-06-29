from pawpal_system import Task, Pet, Owner, Scheduler

# Owner
owner = Owner(name="Alex", available_minutes=120)

# Pets
dog = Pet(name="Buddy", species="Dog", breed="Labrador", age=3)
cat = Pet(name="Luna", species="Cat", breed="Siamese", age=5)

# Tasks added out of order (evening before morning, low before high)
dog.add_task(Task(task_id="t1", name="Evening Walk",    category="exercise",    duration_minutes=25, priority="medium", pet_name="Buddy", preferred_time="6:00pm"))
dog.add_task(Task(task_id="t2", name="Morning Walk",    category="exercise",    duration_minutes=30, priority="high",   pet_name="Buddy", preferred_time="7:15am"))
dog.add_task(Task(task_id="t3", name="Feed Breakfast",  category="feeding",     duration_minutes=10, priority="high",   pet_name="Buddy", preferred_time="8:00am"))

cat.add_task(Task(task_id="t4", name="Evening Playtime", category="enrichment", duration_minutes=20, priority="low",    pet_name="Luna",  preferred_time="6:45pm"))
cat.add_task(Task(task_id="t5", name="Clean Litter Box", category="hygiene",    duration_minutes=15, priority="medium", pet_name="Luna",  preferred_time="9:30am"))
cat.add_task(Task(task_id="t6", name="Feed Dinner",      category="feeding",    duration_minutes=10, priority="high",   pet_name="Luna",  preferred_time="5:00pm", is_completed=True))

# Register pets with owner
owner.add_pet(dog)
owner.add_pet(cat)

# Build schedule
schedule = Scheduler(date="2026-06-29", owner=owner)
schedule.generate_plan()

print("=" * 40)
print("TODAY'S SCHEDULE")
print("=" * 40)
print(schedule.explain_plan())

print("\n" + "=" * 40)
print("SORTED BY TIME")
print("=" * 40)
for t in schedule.sort_by_time():
    print(f"  {t.preferred_time or 'no time':>10}  [{t.priority.upper():^6}]  {t.name} ({t.pet_name})")

print("\n" + "=" * 40)
print("FILTER: Buddy's tasks only")
print("=" * 40)
for t in schedule.filter_tasks(pet_name="Buddy"):
    print(f"  {t.name} — {t.priority}")

print("\n" + "=" * 40)
print("FILTER: Incomplete tasks only")
print("=" * 40)
for t in schedule.filter_tasks(is_completed=False):
    print(f"  {t.name} ({t.pet_name}) — done={t.is_completed}")

print("\n" + "=" * 40)
print("FILTER: Completed tasks only")
print("=" * 40)
for t in schedule.filter_tasks(is_completed=True):
    print(f"  {t.name} ({t.pet_name}) — done={t.is_completed}")

print("\n" + "=" * 40)
print("CONFLICT DETECTION TEST")
print("=" * 40)
# Add two tasks for different pets at the exact same time
schedule.add_task(Task(task_id="c1", name="Brush Teeth",  category="hygiene",  duration_minutes=5, priority="low",    pet_name="Buddy", preferred_time="8:00am"))
schedule.add_task(Task(task_id="c2", name="Morning Meds", category="health",   duration_minutes=5, priority="high",   pet_name="Luna",  preferred_time="8:00am"))

conflicts = schedule.detect_conflicts()
if conflicts:
    for msg in conflicts:
        print(msg)
else:
    print("No conflicts detected.")
