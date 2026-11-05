from datetime import date, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete():
    task = Task("Morning walk", "08:30", 25, 1)

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", "08:30", 25, 1)

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task

def test_sort_by_time():
    scheduler = Scheduler(Owner("Jordan", 45))
    late = Task("Dinner", "17:00", 5, 1)
    early = Task("Breakfast", "08:00", 5, 1)

    assert scheduler.sort_by_time([late, early]) == [early, late]


def test_daily_task_creates_next_occurrence():
    pet = Pet("Mochi", "dog")
    task = Task("Morning walk", "08:30", 25, 1, frequency="daily")
    pet.add_task(task)
    scheduler = Scheduler(Owner("Jordan", 45, pets=[pet]))

    next_task = scheduler.mark_task_complete(pet, task)

    assert task.completed is True
    assert len(pet.tasks) == 2
    assert next_task is pet.tasks[1]
    assert next_task.due_date == date.today() + timedelta(days=1)
    assert next_task.completed is False


def test_detect_conflicts_across_pets():
    dog = Pet("Mochi", "dog")
    cat = Pet("Luna", "cat")
    dog.add_task(Task("Play time", "17:00", 10, 2))
    cat.add_task(Task("Dinner", "17:00", 5, 1))
    scheduler = Scheduler(Owner("Jordan", 45, pets=[dog, cat]))

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "17:00" in warnings[0]
    assert "Mochi: Play time" in warnings[0]
    assert "Luna: Dinner" in warnings[0]