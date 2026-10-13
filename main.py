"""CLI demo for PawPal+. Builds an owner, pets, and tasks, then prints today's schedule."""

from pawpal_system import Owner, Pet, Task, Scheduler


def format_schedule(pairs):
    """Turn (pet, task) pairs into readable schedule lines."""
    lines = []
    for pet, task in pairs:
        status = "done" if task.completed else "todo"
        lines.append(
            f"  {task.time}  {task.description} ({pet.name}) "
            f"[{task.frequency}] [{status}]"
        )
    return "\n".join(lines) if lines else "  (no tasks)"


def main():
    owner = Owner(name="Noah")

    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)

    # Added out of time order on purpose to show sorting works.
    biscuit.add_task(Task("Evening walk", "18:00", frequency="daily"))
    biscuit.add_task(Task("Morning walk", "08:00", frequency="daily"))
    mochi.add_task(Task("Feed", "08:00", frequency="daily"))
    mochi.add_task(Task("Vet appointment", "14:30", frequency="once"))

    scheduler = Scheduler(owner)

    print("Today's Schedule for", owner.name)
    print(format_schedule(scheduler.todays_schedule()))

    print("\nOnly Mochi's tasks:")
    print(format_schedule(scheduler.filter_tasks(pet_name="Mochi")))

    print("\nConflict check:")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            print("  ! " + warning)
    else:
        print("  none")

    print("\nComplete Biscuit's morning walk (daily) -> rolls to tomorrow:")
    morning = biscuit.tasks[1]  # "Morning walk"
    upcoming = scheduler.complete_task(biscuit, morning)
    print(f"  next occurrence due {upcoming.due_date} at {upcoming.time}")


if __name__ == "__main__":
    main()
