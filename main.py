from tabulate import tabulate

from pawpal_system import Task, Pet, Owner, Scheduler

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"

PRIORITY_COLORS = {"high": RED, "medium": YELLOW, "low": GREEN}
PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}
CATEGORY_ICONS = {
    "exercise": "🐾",
    "feeding": "🍖",
    "enrichment": "🧸",
    "hygiene": "🧼",
    "health": "💊",
}


def priority_label(priority: str) -> str:
    icon = PRIORITY_ICONS.get(priority, "⚪")
    color = PRIORITY_COLORS.get(priority, "")
    return f"{color}{icon} {priority.upper()}{RESET}"


def status_label(is_completed: bool) -> str:
    return f"{GREEN}✅ Done{RESET}" if is_completed else f"{CYAN}⏳ Pending{RESET}"


def section(title: str) -> None:
    print(f"\n{BOLD}{MAGENTA}{'=' * 40}{RESET}")
    print(f"{BOLD}{MAGENTA}{title}{RESET}")
    print(f"{BOLD}{MAGENTA}{'=' * 40}{RESET}")


def print_task_table(tasks: list[Task]) -> None:
    rows = []
    for t in tasks:
        icon = CATEGORY_ICONS.get(t.category, "📌")
        rows.append([
            t.preferred_time or "—",
            priority_label(t.priority),
            f"{icon} {t.name}",
            t.pet_name,
            f"{t.duration_minutes} min",
            status_label(t.is_completed),
        ])
    print(tabulate(
        rows,
        headers=["Time", "Priority", "Task", "Pet", "Duration", "Status"],
        tablefmt="rounded_outline",
    ))


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

section("🐶🐱 TODAY'S SCHEDULE")
print_task_table(schedule.sort_tasks())
print(f"\n{BOLD}⏱  Total: {schedule.get_total_duration()} / {schedule.owner.available_minutes} min{RESET}")

section("🕒 SORTED BY TIME")
print_task_table(schedule.sort_by_time())

section("🐕 FILTER: Buddy's tasks only")
print_task_table(schedule.filter_tasks(pet_name="Buddy"))

section("⏳ FILTER: Incomplete tasks only")
print_task_table(schedule.filter_tasks(is_completed=False))

section("✅ FILTER: Completed tasks only")
print_task_table(schedule.filter_tasks(is_completed=True))

section("⚠️  CONFLICT DETECTION TEST")
# Add two tasks for different pets at the exact same time
schedule.add_task(Task(task_id="c1", name="Brush Teeth",  category="hygiene",  duration_minutes=5, priority="low",    pet_name="Buddy", preferred_time="8:00am"))
schedule.add_task(Task(task_id="c2", name="Morning Meds", category="health",   duration_minutes=5, priority="high",   pet_name="Luna",  preferred_time="8:00am"))

conflicts = schedule.detect_conflicts()
if conflicts:
    for msg in conflicts:
        print(f"{RED}⚠️  {msg}{RESET}")
else:
    print(f"{GREEN}✅ No conflicts detected.{RESET}")
