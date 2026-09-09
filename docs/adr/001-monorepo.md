# ADR-001: Start One Serious Project as a Monorepo

## Status

Accepted

## Context

One Serious Project will combine application code, infrastructure code,
Kubernetes configuration, Helm charts, GitOps configuration, observability,
automation, and documentation as its milestones are implemented. At Bootstrap,
the repository contains project structure, engineering workflow, and
documentation; application and infrastructure implementations remain planned.

The project is maintained by one engineer with AI assistance and should be
easy for portfolio reviewers to explore. It needs a repository strategy that
keeps project context together and makes changes across these concerns
manageable with limited maintenance overhead.

## Options Considered

### Option 1 — Monorepo

Application, platform, infrastructure, and documentation live in one repository.
Changes affecting multiple areas can be reviewed together, while those areas
share repository access and history.

### Option 2 — Multiple repositories

Separate repositories hold application code, infrastructure, GitOps
configuration, and possibly observability. This supports distinct permissions
and independent lifecycles, but adds coordination, documentation, and
repository discovery overhead for a one-person team.

## Decision

One Serious Project will begin as a monorepo.

Reasons:

- One source of project context.
- A simpler workflow for a one-person team.
- Easier portfolio navigation.
- Easier cross-cutting changes across application and platform concerns.
- Lower operational overhead.
- Clearer project evolution through a shared history.

Use the existing top-level directories documented in the
[README](../../README.md) to organize application, platform, infrastructure,
automation, and documentation concerns as they are implemented.

## Consequences

### Positive

- Simpler repository discovery for reviewers and contributors.
- Easy local navigation across application and platform concerns.
- A single issue and PR context for related changes.
- Simpler documentation with project knowledge in one place.
- Easier early-stage development for one engineer.

### Negative

- The repository will grow larger as more components are implemented.
- CI will eventually require path filtering to avoid running unrelated checks
  for every change.
- Application and infrastructure changes share repository and access
  boundaries.
- GitOps state may eventually deserve stronger separation from development
  changes.

## Future Considerations

GitOps/environment-state configuration may later be extracted into a separate
repository if the following needs justify the additional complexity:

- Deployment permissions need distinct access controls.
- Environment history needs independent tracking.
- Security boundaries require stronger separation.
- GitOps configuration needs an independent lifecycle.

Make such a split only through an explicit future architecture decision that
weighs its benefits against the additional operational and maintenance
complexity. The monorepo remains the chosen strategy until that decision is
justified and accepted.
