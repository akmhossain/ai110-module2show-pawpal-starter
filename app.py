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

if "pet" not in st.session_state:
    st.session_state.pet = None
if "owner" not in st.session_state:
    st.session_state.owner = None

if st.button("Add pet"):
    pet = Pet(name=pet_name, species=species, breed=breed, age=age)
    owner = Owner(name=owner_name, available_minutes=int(available_minutes))
    owner.add_pet(pet)
    st.session_state.pet = pet
    st.session_state.owner = owner
    st.success(f"Added {pet.name} for owner {owner.name} ({available_minutes} min available).")

st.divider()
st.subheader("Tasks")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3, col4 = st.columns(4)
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
    if st.session_state.pet is None:
        st.error("Add a pet first.")
    else:
        task = Task(
            task_id=str(len(st.session_state.tasks) + 1),
            name=task_title,
            category="general",
            duration_minutes=int(duration),
            priority=priority,
            pet_name=st.session_state.pet.name,
            preferred_time=preferred_time if preferred_time != "(none)" else None,
        )
        st.session_state.tasks.append(task)
        st.session_state.pet.add_task(task)

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

if st.button("Generate schedule"):
    if st.session_state.owner is None or st.session_state.pet is None:
        st.error("Add an owner and pet before generating a schedule.")
    elif not st.session_state.tasks:
        st.error("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler(
            date=str(date.today()),
            owner=st.session_state.owner,
        )
        scheduled = scheduler.generate_plan()

        st.success(f"Scheduled {len(scheduled)} task(s).")

        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for warning in conflicts:
                st.warning(warning)

        st.text(scheduler.explain_plan())

        if scheduled:
            st.markdown("#### Scheduled tasks (sorted by priority & time)")
            st.table(
                [
                    {
                        "name": t.name,
                        "priority": t.priority,
                        "duration (min)": t.duration_minutes,
                        "preferred time": t.preferred_time or "—",
                        "pet": t.pet_name,
                    }
                    for t in scheduler.sort_tasks()
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
