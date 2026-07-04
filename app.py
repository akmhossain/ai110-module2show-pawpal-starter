import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Owner & Pet Setup")

col_owner, col_budget = st.columns(2)
with col_owner:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_budget:
    available_minutes = st.number_input(
        "Owner's available time (minutes)", min_value=10, max_value=720, value=120
    )

col_pet, col_species, col_breed, col_age = st.columns(4)
with col_pet:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_species:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_breed:
    breed = st.text_input("Breed", value="Mixed")
with col_age:
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)

if "pets" not in st.session_state:
    st.session_state.pets = []
if "owner" not in st.session_state:
    st.session_state.owner = None

if st.button("Add pet"):
    pet = Pet(name=pet_name, species=species, breed=breed, age=age)
    if st.session_state.owner is None:
        st.session_state.owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    st.session_state.owner.add_pet(pet)
    st.session_state.pets.append(pet)
    st.success(f"Added {pet.name} for owner {st.session_state.owner.name} "
               f"({st.session_state.owner.available_minutes} min available).")

st.divider()
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if not st.session_state.pets:
    st.info("Add a pet above before creating tasks.")
else:
    col0, col1, col2, col3, col4 = st.columns(5)
    with col0:
        task_pet_name = st.selectbox("Pet", [p.name for p in st.session_state.pets])
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        preferred_time = st.selectbox(
            "Preferred time", ["(none)", "morning", "afternoon", "evening", "night"]
        )

    if st.button("Add task"):
        selected_pet = next(p for p in st.session_state.pets if p.name == task_pet_name)
        task = Task(
            task_id=str(len(st.session_state.tasks) + 1),
            name=task_title,
            category="general",
            duration_minutes=int(duration),
            priority=priority,
            pet_name=selected_pet.name,
            preferred_time=preferred_time if preferred_time != "(none)" else None,
        )
        st.session_state.tasks.append(task)
        selected_pet.add_task(task)

        check_scheduler = Scheduler(date=str(date.today()), owner=st.session_state.owner)
        check_scheduler.tasks = st.session_state.tasks
        conflicts = check_scheduler.detect_conflicts()
        new_conflicts = [w for w in conflicts if task.name in w]
        if new_conflicts:
            for warning in new_conflicts:
                st.warning(warning)
        else:
            st.success(f"Added '{task.name}' with no scheduling conflicts.")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "name": t.name,
                "duration (min)": t.duration_minutes,
                "priority": t.priority,
                "preferred time": t.preferred_time or "—",
                "pet": t.pet_name,
            }
            for t in st.session_state.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None
if "scheduled" not in st.session_state:
    st.session_state.scheduled = []

if st.button("Generate schedule"):
    if st.session_state.owner is None or not st.session_state.pets:
        st.error("Add an owner and pet before generating a schedule.")
    elif not st.session_state.tasks:
        st.error("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(
            date=str(date.today()),
            owner=st.session_state.owner,
        )
        st.session_state.scheduled = scheduler.generate_plan()
        st.session_state.scheduler = scheduler

if st.session_state.scheduler is not None:
    scheduler = st.session_state.scheduler
    scheduled = st.session_state.scheduled

    st.success(f"Scheduled {len(scheduled)} task(s), using "
               f"{scheduler.get_total_duration()}/{scheduler.owner.available_minutes} min "
               f"({'within' if scheduler.is_within_budget() else 'over'} budget).")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(warning)
    else:
        st.success("No scheduling conflicts detected.")

    st.text(scheduler.explain_plan())

    if scheduled:
        sort_choice = st.radio(
            "Sort scheduled tasks by", ["Priority & time", "Time of day"], horizontal=True
        )
        st.markdown("#### Scheduled tasks")
        ordered = scheduler.sort_tasks() if sort_choice == "Priority & time" else scheduler.sort_by_time()
        st.table(
            [
                {
                    "name": t.name,
                    "priority": t.priority,
                    "duration (min)": t.duration_minutes,
                    "preferred time": t.preferred_time or "—",
                    "pet": t.pet_name,
                }
                for t in ordered
            ]
        )

    skipped = [t for t in st.session_state.tasks if t not in scheduled]
    if skipped:
        st.markdown("#### Skipped (didn't fit in time budget)")
        st.table(
            [
                {
                    "name": t.name,
                    "priority": t.priority,
                    "duration (min)": t.duration_minutes,
                }
                for t in skipped
            ]
        )

if st.session_state.get("scheduler") is not None:
    st.divider()
    st.subheader("Filter Scheduled Tasks")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_priority = st.selectbox("Priority", ["(any)", "low", "medium", "high"])
    with col_f2:
        filter_time = st.selectbox(
            "Preferred time", ["(any)", "morning", "afternoon", "evening", "night"]
        )
    with col_f3:
        filter_pet = st.text_input("Pet name filter", value="")

    filtered = st.session_state.scheduler.filter_tasks(
        priority=None if filter_priority == "(any)" else filter_priority,
        preferred_time=None if filter_time == "(any)" else filter_time,
        pet_name=filter_pet or None,
    )

    if filtered:
        st.table(
            [
                {
                    "name": t.name,
                    "priority": t.priority,
                    "duration (min)": t.duration_minutes,
                    "preferred time": t.preferred_time or "—",
                    "pet": t.pet_name,
                }
                for t in filtered
            ]
        )
    else:
        st.info("No scheduled tasks match these filters.")
