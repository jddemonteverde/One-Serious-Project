# AI engineering instructions

`AGENTS.md` is the canonical cross-agent engineering contract for this repository.
All AI coding agents should follow it. `CLAUDE.md` is a short entry point to this
shared guidance.

## 1. Project Purpose

One Serious Project is a production-style DevOps platform and portfolio project,
developed incrementally and maintained initially as a monorepo. It is operated
as a one-person engineering project with AI assistance. The application exists
to support the DevOps and platform engineering demonstration.

The larger goal is to demonstrate application delivery, testing, containers,
CI/CD, Kubernetes, Helm, GitOps, Infrastructure as Code, cloud infrastructure,
observability, security, reliability, incident response, operational
documentation, and cost awareness. These are project goals, not a claim that
every capability is already implemented.

## 2. Current vs Target Architecture

Always distinguish these concepts:

- **Current architecture:** capabilities actually implemented and supported by
  evidence in the repository.
- **Target architecture:** planned capabilities and technologies that may be
  introduced in later tickets and milestones.

At this bootstrap stage, the repository contains its initial structure, shared
configuration, workflow templates, and documentation. Application code,
infrastructure, deployment configuration, and automated checks will be added
as the project develops.

Inspect the repository before claiming a capability exists. Consult the
[README](README.md), [roadmap](docs/roadmap.md), and any existing architecture
documentation and ADRs. Planned technologies must not be represented as
implemented functionality; update descriptions as the implementation evolves.

## 3. Ticket-Driven Development

Meaningful work must correspond to an OSP ticket. Before implementation:

1. Identify the current ticket.
2. Understand its objective.
3. Inspect its implementation tasks.
4. Inspect its acceptance criteria.
5. Identify dependencies and blockers.
6. Inspect the current repository state.

Read `README.md` and relevant documentation before making changes. Use the
[OSP task template](.github/ISSUE_TEMPLATE/task.md) when drafting new tickets.
Do not silently expand ticket scope. Suggest useful unrelated work as a
separate ticket.

## 4. Incremental Engineering

The project is built brick by brick. Do not prematurely introduce technologies
belonging to later milestones:

- Do not introduce Kubernetes during the Application MVP.
- Do not introduce Helm before raw Kubernetes resources exist.
- Do not introduce Argo CD before Kubernetes deployment works.
- Do not introduce AWS infrastructure before the local platform is ready.
- Do not create abstractions purely for hypothetical future requirements.

Prefer the smallest correct implementation that satisfies the current ticket.

## 5. Architecture Decisions

Do not silently make significant architectural decisions. For meaningful
technology or architecture changes, make the following explicit:

- Problem.
- Options considered.
- Selected approach.
- Tradeoffs.
- Operational consequences.

Keep the project owner aware of these choices and their consequences. Recommend
an ADR when appropriate, and record significant architecture decisions in
[docs/adr/](docs/adr/). Routine implementation choices within the agreed ticket
do not need to become new architecture decisions.

## 6. AI Role

AI is an engineering assistant, not the project owner. AI may inspect code,
implement scoped tickets, write tests, review diffs, propose designs, identify
bugs, improve documentation, help investigate incidents, suggest commit
messages, and draft PR descriptions.

AI must not silently take ownership of:

- Architecture decisions.
- Risk acceptance.
- Security policy.
- Cost decisions.
- Incident root cause conclusions.
- Major technology selection.

These remain the project owner's responsibility and require explicit reasoning
and project-owner awareness. Carry out decisions already authorized by the
owner or current ticket; make new significant choices explicit to the owner.

## 7. Code Change Rules

1. Inspect existing files before editing them.
2. Minimize the number of changed files.
3. Avoid unrelated refactoring.
4. Preserve valid existing behavior and instructions.
5. Do not add dependencies without a justification tied to the current ticket.
6. Do not rewrite code solely for stylistic preference.

Use the directory layout documented in `README.md`. Follow `.editorconfig` and
the conventions established in the files you edit.

Empty directories contain `.gitkeep` placeholders. Remove a placeholder when its
directory gains substantive tracked files.

## 8. Testing and Validation

A task is not complete merely because code was written. Before reporting
completion, run the applicable checks:

- Tests.
- Linters.
- Formatters.
- Builds.
- Configuration validation.
- Ticket-specific checks.

Use the commands available in the repository. Include `git status` and
`git diff --check` in the final review, and inspect new files as well as tracked
changes; a plain Git diff does not include untracked files.

Never say a test or other check passed unless it was actually executed
successfully. If a check cannot be run, explicitly state which check, why it
could not run, and what remains unvalidated. Distinguish manual inspection
from automated testing.

## 9. Security Rules

Assume the repository may be public. Never commit:

- Passwords.
- API keys.
- Access tokens.
- Private keys.
- Cloud credentials.
- Real Kubernetes secret values.
- `.env` files containing secrets.
- Terraform variable files containing secrets.

Do not log sensitive values or expose them in command output, documentation,
tests, or examples. Keep local environment files out of version control;
sanitized example files may be committed when needed.

## 10. Commit Message Rules

Use Conventional Commits:

```text
<type>(<scope>): <description>
```

Supported types include `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`,
`build`, `perf`, and `revert`.

Suggested scopes include `app`, `database`, `container`, `ci`, `kubernetes`,
`helm`, `gitops`, `terraform`, `observability`, `security`, `reliability`, `docs`,
and `project`.

Examples:

```text
feat(app): add task creation endpoint
feat(database): add PostgreSQL persistence
ci(app): run tests on pull requests
fix(kubernetes): correct readiness probe
feat(observability): add API latency dashboard
docs(runbook): document database recovery
chore(project): add AI engineering instructions
```

Vague messages such as `update`, `changes`, `fix stuff`, `working`, `final`,
`misc`, and `update files` are forbidden.

Inspect the actual Git diff before proposing a commit message, including new
files and staged changes. The message must describe what changed in the
repository, not what happened in the AI conversation. Do not commit or push
unless explicitly instructed by the project owner.

## 11. Branch Naming

Use ticket-specific branches with lowercase names and hyphens:

```text
<type>/osp-<ticket>-<short-description>
```

Examples:

```text
feature/osp-005-fastapi-scaffold
fix/osp-021-readiness-probe
docs/osp-004-architecture-v0
chore/osp-003-ai-engineering-rules
```

Follow the [development workflow](docs/development/workflow.md) for the canonical
`main` branch policy, pull request flow, and deferred CI-dependent protections.

## 12. Pull Request Expectations

Use this PR title format:

```text
OSP-XXX: <short description>
```

Use the actual OSP ticket identifier followed by a colon and one space. Keep the
description concise and based on the actual Git diff. For example:
`OSP-003: Define AI engineering instructions`.

Use the [pull request template](.github/pull_request_template.md). Descriptions
must cover:

- What changed?
- Why?
- How was it tested?
- Risks.
- Rollback.
- Evidence.
- Related ticket.

Do not fabricate testing, evidence, or ticket links. Replace placeholders with
the correct ticket reference and describe only verification actually performed.

## 13. Documentation

Important operational knowledge must live in the repository, not only in AI
chat history. Update documentation when changes affect architecture, developer
setup, deployment, configuration, operations, security, troubleshooting, cost,
or recovery.

Document new setup steps and development commands in `README.md`. Keep detailed
procedures in the relevant documentation under `docs/` and link them from the
README when needed.

## 14. Infrastructure Principles

Infrastructure should be declared, version controlled, reviewable, repeatable,
destroyable where practical, and cost-aware.

Manual changes must not become undocumented persistent infrastructure. Capture
lasting configuration and operational instructions in the repository as
infrastructure is introduced in the appropriate milestones.

## 15. Reliability Principles

When operational features are introduced, consider:

- How do we know it is healthy?
- How do we know it is unhealthy?
- What metrics expose problems?
- What logs help diagnosis?
- What alert should fire?
- How is it recovered?
- How is it rolled back?

## 16. Definition of Done

A ticket is complete only when:

- Required behavior is implemented.
- Acceptance criteria are met.
- Relevant tests pass.
- Relevant validation passes.
- No secrets were introduced.
- Documentation was updated if required.
- Scope remained controlled.
- Limitations are documented.

If anything cannot be validated, say so explicitly. Identify unresolved
acceptance criteria as outstanding rather than claiming full completion.

## 17. AI Completion Report

Use this structure when reporting completed work:

```text
Ticket:
OSP-XXX

Implemented:
- ...

Validation performed:
- ...

Files changed:
- ...

Architecture/documentation impact:
- ...

Remaining concerns:
- ...

Suggested commit:
<conventional commit message>
```

## 18. Instruction Priority

Resolve repository guidance in this order:

1. Explicit project-owner instructions.
2. Current OSP ticket and acceptance criteria.
3. `AGENTS.md`.
4. Repository documentation.
5. Existing repository conventions.
6. AI recommendations.

When lower-priority guidance conflicts with higher-priority guidance, follow
the higher-priority requirement.
