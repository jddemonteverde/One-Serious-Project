# Project roadmap

## Planned release milestones

These are planned release milestones and may evolve as the project develops.
GitHub milestones are managed separately through GitHub.

- v0.1.0 — Application MVP
- v0.1.5 — Web Frontend
- v0.2.0 — Containers
- v0.3.0 — Continuous Integration
- v0.4.0 — Kubernetes
- v0.5.0 — Helm
- v0.6.0 — GitOps
- v0.7.0 — Observability
- v0.8.0 — Cloud Infrastructure (Terraform, AWS first)
- v0.9.0 — Security and Reliability
- v1.0.0 — Production Simulation

The Web Frontend milestone is numbered `v0.1.5` rather than inserted as a new
minor version. Renumbering the milestones after it would mean editing
[ADR-002](adr/002-terraform-and-cloud-targets.md), which is an accepted decision
record that pins cloud infrastructure to `v0.8.0`, and the
[development workflow](development/workflow.md), which pins required CI checks to
`v0.3.0`. Accepted ADRs record what was decided and are superseded rather than
rewritten, so the existing numbering is left intact.

## Application direction

The application is a personal gamified habit tracker with habits, daily
completions, streaks, points, and badges. It is deliberately small; its purpose
is to provide a realistic workload for the platform milestones. The backend is
FastAPI and the frontend is a separate React application, laid out under
`app/<application>/` so the repository can hold more than one application. See
[ADR-003](adr/003-habit-tracker-domain.md) for the domain decision and
[ADR-004](adr/004-frontend-service-and-application-layout.md) for the frontend
and layout decisions.

## Cloud deployment direction

Terraform is the selected Infrastructure as Code tool. The local platform
milestones come first; v0.8.0 will focus on AWS as the first cloud deployment
target.

The long-term goal is deployment to a choice of AWS, Azure, GCP, or
DigitalOcean. Azure, GCP, and DigitalOcean support will be scoped in future
tickets, with no release assigned yet. See
[ADR-002](adr/002-terraform-and-cloud-targets.md) for the decision and tradeoffs.

## Bootstrap

### Epic 0 — Bootstrap

- OSP-001 — Initialize repository
- OSP-002 — Configure GitHub project workflow
- OSP-003 — Define AI engineering instructions
- OSP-004 — Document architecture v0

## Application

### Epic 1 — Application MVP (v0.1.0)

- OSP-005 — Scaffold FastAPI application
- OSP-013 — Re-scope application domain to a gamified habit tracker
- OSP-006 — Implement Habits API
- OSP-007 — Add PostgreSQL persistence
- OSP-008 — Add database migrations
- OSP-014 — Add habit completions and streak tracking
- OSP-015 — Add points and badges
- OSP-009 — Implement health checks
- OSP-010 — Add structured application logging
- OSP-011 — Expose Prometheus metrics
- OSP-012 — Add automated application tests

### Epic 2 — Web Frontend (v0.1.5)

- OSP-016 — Scaffold React frontend
- OSP-017 — Implement habit management UI
- OSP-018 — Implement gamification UI
- OSP-019 — Add automated frontend tests

Tickets are listed in implementation order, which is not the same as numerical
order. Numbers reflect when a ticket was created.
