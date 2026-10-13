"""PawPal+ Streamlit UI. Connects the Scheduler logic layer to an interactive app."""

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant. Add pets, schedule tasks, see today's plan.")

# --- Application memory ---------------------------------------------------
# Streamlit reruns the script top to bottom on every click, so the Owner must
# live in session_state or it would be rebuilt (and emptied) on each refresh.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Noah")

owner = st.session_state.owner
scheduler = Scheduler(owner)

# --- Add a pet ------------------------------------------------------------
st.subheader("Pets")
with st.form("add_pet", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    if st.form_submit_button("Add pet") and pet_name:
        owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added {pet_name}.")

if owner.pets:
    st.write("Current pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above to get started.")

# --- Add a task -----------------------------------------------------------
if owner.pets:
    st.subheader("Add a Task")
    with st.form("add_task", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            which_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        with c2:
            description = st.text_input("Task", value="Morning walk")
        c4, c5 = st.columns(2)
        with c4:
            task_time = st.text_input("Time (HH:MM)", value="08:00")
        with c5:
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add task") and description:
            pet = next(p for p in owner.pets if p.name == which_pet)
            pet.add_task(Task(description, task_time, frequency=frequency))
            st.success(f"Added '{description}' for {which_pet} at {task_time}.")

st.divider()

# --- Today's schedule -----------------------------------------------------
st.subheader("Today's Schedule")
pairs = scheduler.todays_schedule()

if pairs:
    rows = [
        {
            "Time": task.time,
            "Task": task.description,
            "Pet": pet.name,
            "Frequency": task.frequency,
            "Status": "done" if task.completed else "todo",
        }
        for pet, task in pairs
    ]
    st.table(rows)

    conflicts = scheduler.detect_conflicts()
    for warning in conflicts:
        st.warning(warning)
    if not conflicts:
        st.success("No scheduling conflicts.")

    # --- Complete a task (shows recurrence) ---
    st.subheader("Complete a Task")
    labels = [f"{t.time} {t.description} ({p.name})" for p, t in pairs]
    choice = st.selectbox("Mark complete", labels)
    if st.button("Complete"):
        idx = labels.index(choice)
        pet, task = pairs[idx]
        upcoming = scheduler.complete_task(pet, task)
        if upcoming is not None:
            st.success(
                f"Done. Next '{upcoming.description}' scheduled for "
                f"{upcoming.due_date} at {upcoming.time}."
            )
        else:
            st.success("Done. One-off task, nothing rescheduled.")
        st.rerun()
else:
    st.info("No tasks scheduled yet.")
