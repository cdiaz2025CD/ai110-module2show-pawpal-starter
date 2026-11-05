import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=45)

owner = st.session_state.owner

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    name = pet_name.strip()

    if not name:
        st.warning("Enter a pet name first.")
    else:
        owner.add_pet(Pet(name=name, species=species))
        st.success(f"Added {name}.")

if owner.pets:
    st.write("Your pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")

st.markdown("### Tasks")

if not owner.pets:
    st.info("Add a pet before adding tasks.")
else:
    pet_index = st.selectbox(
        "Choose a pet",
        range(len(owner.pets)),
        format_func=lambda index: f"{index + 1}. {owner.pets[index].name}",
    )
    selected_pet = owner.pets[pet_index]

    task_title = st.text_input("Task title", value="Morning walk")
    task_time = st.time_input("Scheduled time")
    duration = st.number_input("Duration (minutes)", min_value=1, value=20)
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    frequency = st.selectbox("Repeat", ["Once", "Daily", "Weekly"])
    priority_values = {"High": 1, "Medium": 2, "Low": 3}

    if st.button("Add task"):
        if task_title.strip():
            selected_pet.add_task(
                Task(
                    description=task_title.strip(),
                    time=task_time.strftime("%H:%M"),
                    duration=int(duration),
                    priority=priority_values[priority],
                    frequency=frequency.lower(),
                )
            )
            st.success(f"Added task for {selected_pet.name}.")
        else:
            st.warning("Enter a task title first.")

  
    scheduler = Scheduler(owner)
    pending_tasks = scheduler.sort_by_time(
        [task for task in selected_pet.tasks if not task.completed]
    )

    if pending_tasks:
        task_index = st.selectbox(
            "Choose a task to complete",
            range(len(pending_tasks)),
            format_func=lambda index: (
                f"{index + 1}. {pending_tasks[index].description} "
                f"({pending_tasks[index].due_date} at {pending_tasks[index].time})"
            ),
        )

        if st.button("Mark complete"):
            task = pending_tasks[task_index]
            next_task = scheduler.mark_task_complete(selected_pet, task)
            st.success(f"Completed {task.description}.")
            if next_task is not None:
                st.info(f"Next occurrence: {next_task.due_date}")

    status = st.selectbox("Show tasks", ["All", "Pending", "Complete"])
    visible_tasks = selected_pet.tasks

    if status != "All":
        show_completed = status == "Complete"
        visible_tasks = [
            task for task in visible_tasks if task.completed == show_completed
        ]

    if visible_tasks:
        st.table([
            {
                "Task": task.description,
                "Date": str(task.due_date),
                "Time": task.time,
                "Minutes": task.duration,
                "Status": "Complete" if task.completed else "Pending",
            }
            for task in scheduler.sort_by_time(visible_tasks)
        ])
    else:
        st.info("No tasks match this filter.")

st.divider()

st.subheader("Build Schedule")

owner.name = owner_name.strip() or "Jordan"
owner.available_minutes = int(
    st.number_input("Available minutes today", min_value=0, value=45)
)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan = scheduler.generate_plan()

    for warning in scheduler.detect_conflicts():
        st.warning(warning)

    if not plan:
        st.info("No unfinished tasks due today fit your available time.")
    else:
        total_minutes = sum(task.duration for task in plan)
        st.success(
            f"{owner.name}'s plan uses {total_minutes} "
            f"of {owner.available_minutes} minutes."
        )
        st.caption(
            "The scheduler considers higher priorities first "
            "and displays the selected tasks in time order."
        )
        st.table([
            {
                "Time": task.time,
                "Task": task.description,
                "Minutes": task.duration,
                "Priority": {1: "High", 2: "Medium", 3: "Low"}[task.priority],
            }
            for task in plan
        ])
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""    
