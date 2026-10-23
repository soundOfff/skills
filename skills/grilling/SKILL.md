---
name: grilling
description: Interview the user relentlessly about a plan, decision, or idea, asking every question that can be settled now in one numbered round at a time. Use when the user wants to stress-test their thinking or a design, or uses any 'grill' trigger phrase.
---

Interview the user relentlessly until you reach a shared understanding. Map the plan as a **design tree**, where every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled. These are the questions you can ask *now* without guessing at answers you have not heard yet. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the user's answers before the next round.

Each round of answers reshapes the tree. Settled decisions push the frontier outward and unblock the questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a *later* round, not this one.

Finding *facts* is your job, never the user's. When a frontier question needs a fact from the environment (the filesystem, tools, the repository), dispatch the `flow-fact-lookup` agent with that one narrow question. When the agent type is missing, use the fallback in [dispatch.md](../flow-mode/references/dispatch.md). Never ask the user for anything you could look up yourself. Do not block on a lookup. A running lookup is an unsettled prerequisite, so only the questions downstream of it wait for its report. Ask the rest of the frontier now. The *decisions* are the user's. Put each one to them and wait.

The session is done when the frontier is empty. Every branch of the design tree has been visited, and nothing is left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
