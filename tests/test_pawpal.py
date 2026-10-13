"""Test suite for PawPal+ core behaviors and scheduling algorithms."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def _owner_with_tasks():
    """Build a small owner/pet/task fixture used by several tests."""
    owner = Owner(name="Noah")
    biscuit = Pet(name="Biscuit", species="dog")
    mochi = Pet(name="Mochi", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(mochi)
    biscuit.add_task(Task("Evening walk", "18:00", frequency="daily"))
    biscuit.add_task(Task("Morning walk", "08:00", frequency="daily"))
    mochi.add_task(Task("Feed", "08:00", frequency="daily"))
    return owner, biscuit, mochi


def test_mark_complete_changes_status():
    task = Task("Walk", "08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_count():
    pet = Pet(name="Biscuit", species="dog")
    assert pet.task_count() == 0
    pet.add_task(Task("Feed", "09:00"))
    assert pet.task_count() == 1


def test_sort_is_chronological():
    owner, _, _ = _owner_with_tasks()
    times = [task.time for _, task in Scheduler(owner).todays_schedule()]
    assert times == sorted(times)
    assert times[0] == "08:00"
    assert times[-1] == "18:00"


def test_filter_by_pet_and_status():
    owner, biscuit, _ = _owner_with_tasks()
    scheduler = Scheduler(owner)
    only_biscuit = scheduler.filter_tasks(pet_name="Biscuit")
    assert len(only_biscuit) == 2
    assert all(pet.name == "Biscuit" for pet, _ in only_biscuit)
    assert scheduler.filter_tasks(completed=True) == []


def test_daily_completion_creates_next_day_task():
    owner, biscuit, _ = _owner_with_tasks()
    scheduler = Scheduler(owner)
    morning = biscuit.tasks[1]
    before = biscuit.task_count()
    upcoming = scheduler.complete_task(biscuit, morning)
    assert morning.completed is True
    assert biscuit.task_count() == before + 1
    assert upcoming.due_date == date.today() + timedelta(days=1)
    assert upcoming.completed is False


def test_once_task_does_not_recur():
    pet = Pet(name="Mochi", species="cat")
    owner = Owner(name="Noah", pets=[pet])
    vet = Task("Vet appointment", "14:30", frequency="once")
    pet.add_task(vet)
    scheduler = Scheduler(owner)
    upcoming = scheduler.complete_task(pet, vet)
    assert upcoming is None
    assert pet.task_count() == 1


def test_conflict_detection_flags_same_time():
    owner, _, _ = _owner_with_tasks()
    conflicts = Scheduler(owner).detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflict_when_times_differ():
    pet = Pet(name="Mochi", species="cat")
    owner = Owner(name="Noah", pets=[pet])
    pet.add_task(Task("Feed", "08:00"))
    pet.add_task(Task("Play", "12:00"))
    assert Scheduler(owner).detect_conflicts() == []


def test_empty_owner_has_empty_schedule():
    owner = Owner(name="Noah")
    assert Scheduler(owner).todays_schedule() == []
