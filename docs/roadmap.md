# Project roadmap

## Planned release milestones

These are planned release milestones and may evolve as the project develops.
GitHub milestones are managed separately through GitHub.

- v0.1.0 — Application MVP
- v0.2.0 — Containers
- v0.3.0 — Continuous Integration
- v0.4.0 — Kubernetes
- v0.5.0 — Helm
- v0.6.0 — GitOps
- v0.7.0 — Observability
- v0.8.0 — Cloud Infrastructure (Terraform, AWS first)
- v0.9.0 — Security and Reliability
- v1.0.0 — Production Simulation

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
