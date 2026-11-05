# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```text
Today's Schedule
08:00 - Breakfast (5 min)
08:30 - Morning walk (25 min)
17:00 - Play time (10 min)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
py -m pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```text
Today's Schedule
08:00 - Breakfast (5 min)
08:30 - Morning walk (25 min)
17:00 - Play time (10 min)

Mochi's unfinished tasks:
08:30 - Morning walk
17:00 - Play time

Next Morning walk: 2026-11-06
Warning: 2026-11-05 at 17:00 - Mochi: Play time conflicts with Luna: Dinner.
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method | Behavior |
|---|---|---|
| Sorting | `sort_by_time()` | Orders tasks by due date, then start time. |
| Filtering | `filter_tasks()` | Filters tasks by pet name, completion status, or both. |
| Conflict detection | `detect_conflicts()` | Warns when unfinished tasks share the same date and start time. |
| Recurring tasks | `mark_task_complete()` | Creates the next occurrence when a daily or weekly task is completed. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Open PawPal+, enter a pet name, choose its species, and click **Add pet**.
2. Select the pet, enter a task title, time, duration, and priority, then choose how often it repeats. Click **Add task**.
3. Enter your available minutes and click **Generate schedule**. PawPal+ considers higher-priority tasks first, then displays the tasks that fit in chronological order. It warns you if unfinished tasks share a start time on the same date.
4. Select a task and click **Mark complete**. Completing a daily or weekly task creates its next occurrence. Use **Show tasks** to switch between all, pending, and completed tasks.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
