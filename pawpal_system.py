from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    description: str
    time: str
    duration: int
    priority: int
    frequency: str = "daily"
    completed: bool = False
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet."""
        self.tasks.append(task)


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Collect tasks from all of this owner's pets."""
        all_tasks = []

        for pet in self.pets:
            all_tasks.extend(pet.tasks)

        return all_tasks


@dataclass
class Scheduler:
    owner: Owner

    def sort_tasks(self) -> list[Task]:
        """Sort unfinished tasks due today by priority, then time."""
        today = date.today()
        tasks = []

        for task in self.owner.get_all_tasks():
            if not task.completed and task.due_date == today:
                tasks.append(task)

        return sorted(
            tasks,
            key=lambda task: (task.priority, task.time)
        )

    def generate_plan(self) -> list[Task]:
        """Choose tasks that fit within the owner's available minutes."""
        remaining_minutes = self.owner.available_minutes
        plan = []

        for task in self.sort_tasks():
            if task.duration <= remaining_minutes:
                plan.append(task)
                remaining_minutes -= task.duration

        return sorted(plan, key=lambda task: task.time)