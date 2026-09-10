# ADR-002: Use Terraform and Introduce Cloud Targets Starting with AWS

## Status

Accepted — project-owner direction recorded in the OSP-004 architecture
documentation follow-up.

## Context

The initial target architecture left the Infrastructure as Code tool choice
open between Terraform and OpenTofu and described AWS as the cloud target.
The project owner has selected Terraform and wants the project to eventually
be deployable to a choice of AWS, Azure, GCP, or DigitalOcean, starting with
AWS.

The project is maintained by one engineer and is still in Bootstrap. Cloud
infrastructure will follow a working local platform. The architecture needs
a clear first cloud scope and a documented direction for additional targets.

## Options Considered

| Decision | Options | Selected approach |
| --- | --- | --- |
| Infrastructure as Code tool | Terraform or OpenTofu | Terraform, as selected by the project owner. |
| Cloud rollout | AWS only; AWS followed by other clouds; all four clouds together | AWS first, with Azure, GCP, and DigitalOcean support added incrementally. |

## Decision

- Use Terraform as the project's Infrastructure as Code tool.
- Establish the local platform before implementing cloud infrastructure.
- Focus the first cloud milestone, v0.8.0, on AWS.
- Keep deployment to Azure, GCP, and DigitalOcean as future goals, scoped
  through later tickets. No release is assigned to those targets yet.
- Introduce each cloud's Terraform configuration and deployment validation
  when that cloud enters scope. Shared infrastructure abstractions will be
  considered only when implemented requirements justify them.

## Consequences

### Positive

- One Infrastructure as Code tool keeps learning and maintenance focused.
- A first implementation on AWS limits the initial cloud work to one provider.
- Future cloud targets are explicit and can be planned incrementally.

### Tradeoffs and Operational Consequences

- Azure, GCP, and DigitalOcean deployments will remain unavailable until their
  implementation and validation tickets are completed.
- Each additional cloud will require infrastructure configuration, deployment
  validation, operational documentation, and cost review for that provider.
- Reuse across clouds will need to be evaluated as those implementations
  develop; Terraform does not make AWS resource definitions interchangeable
  with another provider's resources.

## Deferred Decisions

Specific cloud services, Kubernetes and PostgreSQL hosting, Terraform state
storage and access controls, and any shared module structure will be decided
in the relevant implementation tickets. This ADR records target direction;
no cloud infrastructure is implemented at Bootstrap.

See the [architecture overview](../architecture/overview.md) and
[roadmap](../roadmap.md) for the planned system and milestone sequence.
