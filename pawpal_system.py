from dataclasses import dataclass, field, replace
from datetime import date, timedelta


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

        return self.sort_by_time(plan)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks in chronological order."""
        return sorted(tasks, key=lambda task: (task.due_date, task.time))

    def filter_tasks(
        self,
        pet_name: str | None = None,
        completed: bool | None = None,
    ) -> list[Task]:
        """Return tasks that match the selected pet and completion status."""
        tasks = []

        for pet in self.owner.pets:
            if pet_name is not None and pet.name != pet_name:
                continue

            for task in pet.tasks:
                if completed is None or task.completed == completed:
                    tasks.append(task)

        return tasks
    
    def mark_task_complete(self, pet: Pet, task: Task) -> Task | None:
        """Complete a task and add its next occurrence if it repeats."""
        if task.completed:
            return None

        task.mark_complete()
        days_until_next = {"daily": 1, "weekly": 7}.get(task.frequency)

        if days_until_next is None:
            return None

        next_task = replace(
            task,
            due_date=date.today() + timedelta(days=days_until_next),
            completed=False,
        )
        pet.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> list[str]:
        """Warn when unfinished tasks share a date and start time."""
        first_task_by_slot = {}
        warnings = []

        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed:
                    continue

                slot = (task.due_date, task.time)
                label = f"{pet.name}: {task.description}"

                if slot in first_task_by_slot:
                    warnings.append(
                        f"{task.due_date} at {task.time} - "
                        f"{first_task_by_slot[slot]} conflicts with {label}."
                    )
                else:
                    first_task_by_slot[slot] = label

        return warnings