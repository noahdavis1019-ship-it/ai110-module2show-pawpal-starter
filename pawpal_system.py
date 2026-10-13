"""PawPal+ logic layer. Core classes that model owners, pets, tasks, and the scheduler."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity with a time, frequency, and completion flag."""

    description: str
    time: str  # "HH:MM" 24-hour
    frequency: str = "once"  # once | daily | weekly
    completed: bool = False

    def mark_complete(self):
        """Flip this task's status to completed."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the list of care tasks that belong to it."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Attach a Task to this pet."""
        self.tasks.append(task)

    def task_count(self):
        """Return how many tasks this pet currently has."""
        return len(self.tasks)


@dataclass
class Owner:
    """An owner who manages one or more pets."""

    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Register a pet under this owner."""
        self.pets.append(pet)

    def all_tasks(self):
        """Return a flat list of (pet, task) pairs across every pet."""
        pairs = []
        for pet in self.pets:
            for task in pet.tasks:
                pairs.append((pet, task))
        return pairs


class Scheduler:
    """The brain: reads across the owner's pets to organize and report tasks."""

    def __init__(self, owner):
        """Hold a reference to the owner whose tasks we schedule."""
        self.owner = owner

    def _all_pairs(self):
        """Internal helper: every (pet, task) pair from the owner."""
        return self.owner.all_tasks()

    def sort_by_time(self, pairs=None):
        """Return (pet, task) pairs sorted chronologically by the task's HH:MM time."""
        if pairs is None:
            pairs = self._all_pairs()
        return sorted(pairs, key=lambda pair: pair[1].time)

    def filter_tasks(self, pet_name=None, completed=None):
        """Return (pet, task) pairs filtered by pet name and/or completion status."""
        pairs = self._all_pairs()
        if pet_name is not None:
            pairs = [p for p in pairs if p[0].name == pet_name]
        if completed is not None:
            pairs = [p for p in pairs if p[1].completed == completed]
        return pairs

    def todays_schedule(self):
        """Return all of today's tasks as (pet, task) pairs, time-sorted."""
        return self.sort_by_time()
