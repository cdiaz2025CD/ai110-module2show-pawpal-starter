from pawpal_system import Pet, Task


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