# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions: produce daily plans with actions, add pets and associated tasks, add owner preferences

- Briefly describe your initial UML design.
  My UML incorporates four classes that help owners keep track of thier pet's associated tasks in a schedule. A owner can have multiple pets. Each task is tied to a pet and a schedule is made up of one or many tasks.

- What classes did you include, and what responsibilities did you assign to each?
  I included a owner, pet, task, and schedule class. The owner can own one or more pets, tht pet can have one or more tasks, and a schedule can have one or more task. The owner only has one schedule generated at a time, since they only need one for one day.

**b. Design changes**

- Did your design change during implementation?
  Yes.
- If yes, describe at least one change and why you made it.
  Initially my schedule class had both owner and pet, but that was redudundant so I removed pet. I also added a link to the pet in the task class.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  The scheduler considers time and pirority.
- How did you decide which constraints mattered most?
  I considered time and pirority because they were the most basic and easy to implement.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  generate_plan doesn't account for overlap, only way to detect overlap is through detect_conflict after a plan is generated. It makes the plan simpler instead of adding multiple tasks.
- Why is that tradeoff reasonable for this scenario?
  The user can use the sort by task and detect conflict methods to easily see which methods overlap, and pick the one they perfer. This adds user choice and prevents additional complexity in the logic.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  I used AI to help build the UML diagram and brainstorm features, implement a skeleton of the UML diagram, and debug errors in the UI and CLI.
- What kinds of prompts or questions were most helpful?
  Asking AI to show a preview before implementing was helpful because I can ask it to dissect any part I didn't understand.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  When implementing the UML diagram the AI added methods that were not relevant to the class. For instance, for the pet class there was a owner attribute, which would be redundant. I went through these attributes and relationships and chose only releveant ones.
- How did you evaluate or verify what the AI suggested?
  I made sure that everything played a role and made sense. Then I would test the new code visually or using pytest to see if it reflected the changes I requested.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  I primarly tested behaviours regarding tasks, for instance, adding reccurences and marking complete. All the tasks can be found in tests/test_pawpal.py.
- Why were these tests important?
  It is important to make sure the backend logic runs as intended, so it doesn't fail in the real world.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  4.5/5 because tests ensure that functions work properly in multiple scenarios, whether something is added or not. However, without actually using the app in production we won't truly test to its limits.
- What edge cases would you test next if you had more time?
  I would test the upper bounds of the program, such as the maximum pets or tasks before the program crashes or the UI is too crowded. Then I would implement a cap on the amount allowed based on a reasonable amount.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  I am satisfied to have a better understanding of how to build system architecture. Building the architecture made everything organized from the start, so the actual implementation was a smoother process.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  There were methods that I didnt implement in the UI regarding time represented by strings. So far, the app only uses time zones like morning or evening.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  Starting new sessions each time for separate tasks is better because it reduces the complexity of the prompt, allowing the AI to focus with a fresh start, which may reduce token usage too.
