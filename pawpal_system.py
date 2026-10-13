"""PawPal+ logic layer (skeleton). Classes and empty method stubs from the UML."""

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care activity."""

    description: str
    time: str  # "HH:MM"
    frequency: str = "once"  # once | daily | weekly
    completed: bool = False

    def mark_complete(self):
        """Mark this task as done."""
        ...


@dataclass
class Pet:
    """A pet and the tasks that belong to it."""

    name: str
    species: str
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Attach a task to this pet."""
        ...

    def task_count(self):
        """Return how many tasks this pet has."""
        ...


@dataclass
class Owner:
    """An owner and their pets."""

    name: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Register a pet under this owner."""
        ...

    def all_tasks(self):
        """Return every task across all pets."""
        ...


class Scheduler:
    """The brain: reads across the owner's pets to organize tasks."""

    def __init__(self, owner):
        self.owner = owner

    def todays_schedule(self):
        """Return today's tasks, time-sorted."""
        ...

    def sort_by_time(self, tasks):
        """Return tasks sorted by their HH:MM time."""
        ...

    def filter_tasks(self, pet_name=None, completed=None):
        """Return tasks filtered by pet name and/or completion status."""
        ...

    def detect_conflicts(self):
        """Return warnings for tasks scheduled at the same time."""
        ...
