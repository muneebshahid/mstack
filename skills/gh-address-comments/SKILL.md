---
name: gh-address-comments
description: Help address review/issue comments on the open GitHub PR for the current branch using gh CLI; verify gh auth first and prompt the user to authenticate if not logged in.
metadata:
  short-description: Address comments in a GitHub PR review
---

# PR Comment Handler

Guide to find the open PR for the current branch and address its comments with gh CLI. Run all `gh` commands with elevated network access.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

## 1) Inspect comments needing attention
- Run scripts/fetch_comments.py which will print out all the comments and review threads on the PR

## 2) Determine the addressing scope
- Number all review threads and comments and summarize the required change for each actionable item.
- By default, address every actionable unresolved comment. Do not ask the user to select comments.
- If the user explicitly names a subset, address only that subset.
- Ask for clarification only when a comment itself is ambiguous, requires a material product decision, or would expand beyond the authority of the active request.

## 3) Apply fixes
- Apply fixes for every comment in the determined scope.
- Verify the resulting changes and summarize each comment addressed, any comment that required no change, and any unresolved blocker.

Notes:
- If gh hits auth/rate issues mid-run, prompt the user to re-authenticate with `gh auth login`, then retry.
