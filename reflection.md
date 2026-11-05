# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- I started with four classes in my UML diagram: `Owner`, `Pet`, `Task`, and `Scheduler`. An owner could have multiple pets, and each pet had its own list of tasks. Each task stored details like its start time, duration, priority, and completion status. The scheduler gathered tasks from the owner’s pets and built a daily plan based on priority and how much time the owner had available. Keeping the scheduling logic separate from the Streamlit interface let me test the plan in the terminal before connecting it to the app.
**b. Design changes**

- I added a `due_date` field to the `Task` class so the scheduler could tell when each occurrence was due. When I marked Mochi’s morning walk complete on November 5, PawPal+ kept the original walk marked as complete and created a separate pending walk for November 6. This let the app keep a record of completed tasks while still scheduling the next walk.

### Core User Actions

1. Add a pet and save its basic information.
2. Add or edit pet care tasks, including duration and priority.
3. Generate a daily care plan based on available time and task priorities.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers unfinished tasks due today and checks how many minutes the owner has available. It tries higher-priority tasks first and uses the earlier start time to break ties. If a task takes longer than the remaining time, the scheduler skips it and checks the next one. The final plan is displayed in time order so the owner can see what to do throughout the day.

**b. Tradeoffs**

- I kept conflict detection simple by checking whether two unfinished tasks have the same date and start time. This caught the conflict between Mochi’s play time and Luna’s dinner because both started at 17:00. The tradeoff is that tasks can overlap even when they start at different times. For example, a 30-minute walk at 8:30 would overlap with a feeding at 8:45 without triggering a warning. A future version could use each task’s duration to calculate its end time and catch those overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- I used ChatGPT as a guide while building PawPal+. It helped me break the project into smaller steps, understand how the Python classes worked together, and troubleshoot errors. For example, when the next morning walk didn’t appear in the terminal, I shared my code and got help spotting that the completion call was inside a loop. I moved it outside the loop, ran the program again, and checked that the walk was scheduled for the next day.

**b. Judgment and verification**

-When I added the task filter, I checked how it behaved in the browser. The first version I pasted had some lines indented under the button checks, which meant the filter depended on a button click. I moved those lines so they run whenever a pet is selected. Then I switched the filter without clicking Add task or Mark complete and confirmed that the table updated on its own.

---

## 4. Testing and Verification

**a. What you tested**

- I ran five automated tests with `py -m pytest`, and all five passed. The tests checked that a pet can receive a task, a task can be marked complete, tasks appear in chronological order, a daily task creates a new pending occurrence for the next day, and two pets’ tasks at the same start time trigger a conflict warning. 
- I also tested the Streamlit app by completing a daily task and switching between the Pending and Complete filters to check that each occurrence appeared under the right status.
**b. Confidence**

- I’d give the scheduler 4 out of 5 stars. All five automated tests passed, and I confirmed in the browser that completing a daily task creates a new pending task for the next day. I’d still add automated tests for weekly repeats, a pet with no tasks, and a time budget too small to fit any task.
---

## 5. Reflection

**a. What went well**

- I’m most satisfied with getting recurring tasks to work in the browser. When I marked a daily walk complete, today’s walk stayed in the table as complete and tomorrow’s walk appeared as pending. I could switch between the two filters and see each task under the right status.

**b. What you would improve**

- I would improve conflict detection by using each task’s duration to calculate its end time. Right now, PawPal+ catches tasks that start at the same time. With end times, it could also warn me when a feeding starts before a walk is supposed to finish.

**c. Key takeaway**

- I learned that testing one part at a time made it easier to figure out where a problem was coming from. I tested the scheduler in the terminal first, then checked how it behaved in Streamlit. When I got stuck, I used ChatGPT to help me understand the issue and reran the program myself to see whether the fix worked.
