---
name: sharpen
description: "Make a task deeper, not bigger, then rewrite its prompt. Use only when the user explicitly asks to sharpen a task or prompt."
---

# Sharpen

Deepen the user's task without enlarging its scope. Before rewriting it, answer four questions:

1. What would a top professional in this field do here that the user is not asking for?
2. What is the rawest material they would start from, instead of what has already been digested for the user?
3. Which specific methods and tools would they use?
4. What, other than the agent or the user, would show that the result is right?

Then rewrite the user's prompt to ask for exactly that. Leave the user's own choices open instead of deciding them. Do not start the task; return the answers and the rewritten prompt.
