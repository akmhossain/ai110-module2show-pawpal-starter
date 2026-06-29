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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  generate_plan doesn't account for overlap, only way to detect overlap is through detect_conflict after a plan is generated. It makes the plan simpler instead of adding multiple tasks.
- Why is that tradeoff reasonable for this scenario?
  The user can use the sort by task and detect conflict methods to easily see which methods overlap, and pick the one they perfer. This adds user choice and prevents additional complexity in the logic.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
