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


if __name__ == "__main__":
    main()