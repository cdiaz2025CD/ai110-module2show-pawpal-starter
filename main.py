from pawpal_system import Owner, Pet, Scheduler, Task


def main():
    owner = Owner(name="Jordan", available_minutes=45)

    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Morning walk", "08:30", 25, 1))
    dog.add_task(Task("Play time", "17:00", 10, 2))
    cat.add_task(Task("Breakfast", "08:00", 5, 1))

    scheduler = Scheduler(owner)

    print("Today's Schedule")
    for task in scheduler.generate_plan():
        print(f"{task.time} - {task.description} ({task.duration} min)")

    print("\nMochi's unfinished tasks:")
    mochi_tasks = scheduler.filter_tasks(pet_name="Mochi", completed=False)
    for task in scheduler.sort_by_time(mochi_tasks):
        print(f"{task.time} - {task.description}")

    next_walk = scheduler.mark_task_complete(dog, dog.tasks[0])
    if next_walk is not None:
        print(f"\nNext {next_walk.description}: {next_walk.due_date}")
        cat.add_task(Task("Dinner", "17:00", 5, 1))

    for warning in scheduler.detect_conflicts():
        print(f"Warning: {warning}")


if __name__ == "__main__":
    main()