# Development workflow

Use the [OSP task template](../../.github/ISSUE_TEMPLATE/task.md) to define the
outcome, implementation tasks, and acceptance criteria for each ticket. Use the
[pull request template](../../.github/pull_request_template.md) to describe the
implementation, testing actually performed, risks, and rollback plan for review.

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
