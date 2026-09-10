# Development workflow

Use the [OSP task template](../../.github/ISSUE_TEMPLATE/task.md) to define the
outcome, implementation tasks, and acceptance criteria for each ticket. Use the
[pull request template](../../.github/pull_request_template.md) to describe the
implementation, testing actually performed, risks, and rollback plan for review.

## GitHub Project board

Track OSP tickets in the
[One Serious Project board](https://github.com/users/jddemonteverde/projects/1).
The board uses the existing Status options below:

| Status | When to use it |
| --- | --- |
| `Todo` | Work that has not started, including backlog items and tickets ready for implementation. |
| `Blocked` | Work that cannot proceed because of a dependency or unresolved problem. Record the blocker in the issue. |
| `On-hold` | Work deliberately paused or deferred. Record the reason in the issue. |
| `In Progress` | Active implementation or a pull request awaiting review or merge. |
| `Done` | Acceptance criteria and required validation are verified, with the implementation merged when applicable. |

There are no separate `Backlog`, `Ready`, or `Review` columns. Use `Todo` for
unstarted work and check the issue's Dependencies before beginning; being in
`Todo` does not mean all prerequisites are complete. Move a ticket to
`In Progress` when work starts and keep it there during pull request review.
Use `Blocked` or `On-hold` when appropriate, then return the ticket to `Todo` or
`In Progress` according to whether work is resuming immediately.

Add each issue to the project once and keep its Status aligned with actual
progress. Verify completion from repository and GitHub evidence before using
`Done`; a closed issue alone is not proof that its acceptance criteria are met.
These are working conventions and do not imply that status transitions are
automated.

Application MVP tickets (OSP-005 through OSP-012) use the
`v0.1.0 - Application MVP` GitHub milestone. Bootstrap tickets do not use that
release milestone. Planned releases are listed in the [roadmap](../roadmap.md).

## Main branch policy

- `main` is the canonical branch.
- Meaningful work should happen on ticket-specific branches.
- Feature work should normally reach `main` through pull requests.
- Direct pushes to `main` should be avoided.
- CI checks will become mandatory once the Continuous Integration milestone
  (`v0.3.0`) is implemented.
- Force pushes to `main` should not be used.
- Branch protection will be configured when required checks exist.

Branch protection is intentionally deferred until CI checks are available.
The policy above describes current working practices; CI-dependent enforcement
is planned and is not yet configured.

## Branch naming

Include the work type, ticket identifier, and a short description in the branch
name. Examples:

```text
feature/osp-005-fastapi-scaffold
fix/osp-021-readiness-probe
docs/osp-004-architecture-v0
chore/osp-002-github-workflow
```
