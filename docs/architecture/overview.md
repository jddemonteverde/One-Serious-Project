# Architecture Overview

## 1. Purpose

This document records the **Current Architecture** and **Target Architecture**
of One Serious Project. The target architecture represents direction rather
than current implementation. The project is built incrementally, and claims
about implemented capabilities must be supported by repository evidence.

## 2. Current Architecture

The repository is in **v0.1.0 — Application MVP**, with the first Web Frontend
ticket also delivered. Epic 0 — Bootstrap is complete, and two runtime
components exist: a FastAPI backend and a React frontend, both run locally by a
developer. There is no datastore, container, pipeline, or cloud infrastructure
yet.

```mermaid
flowchart TD
  developer["Developer"] -->|make run| backend["FastAPI backend (local process)"]
  developer -->|make frontend-dev| frontend["React frontend (local dev server)"]
  frontend -->|Proxied API requests| backend
  developer --> repository["Git repository"]
  repository -->|Application source| backend
  repository -->|Application source| frontend
  repository --> workflow["Project structure and engineering workflow"]
```

What exists today:

- A FastAPI backend at `app/habit-tracker/backend/`, whose Python package is
  `habit_tracker`, with a `GET /` endpoint that returns the service name,
  running state, and environment name.
- Backend configuration read from `APP_ENV`, `APP_HOST`, `APP_PORT`,
  `LOG_LEVEL`, and `CORS_ALLOWED_ORIGINS`, with pinned runtime dependencies in
  `app/habit-tracker/backend/requirements.txt`.
- A React and TypeScript frontend at `app/habit-tracker/frontend/` that reads
  and displays the backend's service status, with pinned dependencies and a
  development-server proxy that keeps API calls same-origin.
- A `Makefile` providing `make help`, `make install`, `make run`, and the
  `frontend-install`, `frontend-dev`, `frontend-build`, and `frontend-lint`
  commands, with an `APP` variable selecting which application under `app/` the
  commands act on.
- A monorepo directory structure with reserved component directories.
- Shared repository configuration in `.editorconfig` and `.gitignore`, and a
  license.
- Project documentation, a roadmap, and engineering guidance in `README.md`,
  `AGENTS.md`, and `CLAUDE.md`.
- Issue and pull request templates, plus a documented development workflow.
- This architecture overview and accepted decisions for the
  [monorepo](../adr/001-monorepo.md),
  [Terraform and cloud targets](../adr/002-terraform-and-cloud-targets.md), the
  [habit tracker domain](../adr/003-habit-tracker-domain.md), and the
  [frontend service and application layout](../adr/004-frontend-service-and-application-layout.md).

The backend holds no state and exposes no domain resource, and the frontend has
no habit features. The habit tracker domain, its database, health checks,
metrics, and automated test coverage are the remaining Application MVP tickets;
the habit and gamification interfaces and the frontend test suite are the
remaining Web Frontend tickets. The frontend has no automated tests, and the
backend has no linter. Logging currently uses the standard library default format, not the
structured format planned for log aggregation. The infrastructure, deployment,
observability, automation, and test directories contain placeholders.
`.github/workflows/` also contains only a placeholder; CI jobs have not been
implemented. The documented [development workflow](../development/workflow.md)
defers required CI checks and branch protection until CI is available.

## 3. Target Architecture — Planned

The delivery, runtime, observability, and infrastructure capabilities below
are planned. The developer and GitHub repository provide their existing
starting point. Components will be introduced incrementally through the
[project milestones](../roadmap.md).

The views below each show one part of the target architecture. Read each
diagram from top to bottom; repeated components refer to the same system.

### 3.1 Application Runtime — Planned

The habit tracker runs as two services. A React frontend serves the browser and
calls the FastAPI backend, which stores data in PostgreSQL. Kubernetes will run
both, first locally with kind and later on AWS. PostgreSQL hosting remains a
decision for a later ticket.

```mermaid
flowchart TD
  browser["Browser"] -->|Page requests| frontend["React frontend on Kubernetes"]
  browser -->|API requests| backend["FastAPI backend on Kubernetes"]
  frontend -->|Served assets| browser
  backend -->|Read and write data| postgres[("PostgreSQL")]
```

Each service is deployed and scaled independently. Routing browser traffic to
the frontend and API traffic to the backend is an ingress concern decided in the
Kubernetes milestone. See
[ADR-004](../adr/004-frontend-service-and-application-layout.md).

### 3.2 Build and Deployment — Planned

A developer pushes changes to the monorepo. One path builds and publishes
container images; the other supplies the desired deployment configuration.
Both paths meet at the Kubernetes cluster.

```mermaid
flowchart TD
  repository["GitHub monorepo"] -->|Backend and frontend code| actions["GitHub Actions"]
  actions -->|Validate and publish| registry["GHCR"]
  repository -->|Deployment files| gitops["GitOps configuration"]
  gitops -->|Desired state| argocd["Argo CD"]
  argocd -->|Reconcile workloads| kubernetes["Kubernetes"]
  registry -->|Container images| kubernetes
```

GitHub Actions validates code, builds images, and publishes them to GitHub
Container Registry (GHCR). GitOps configuration lives in the same monorepo and
records the desired workloads and image references, using raw Kubernetes
resources first and Helm charts later. Argo CD reconciles that configuration;
Kubernetes pulls the referenced images from GHCR. The mechanism for updating
image references in Git remains a decision for a later ticket.

### 3.3 Cloud Infrastructure — Planned

Terraform is the selected Infrastructure as Code tool. AWS is the first cloud
target, introduced after the local platform is ready.

```mermaid
flowchart TD
  terraform["Terraform"] -->|Provision resources| aws["AWS infrastructure"]
  aws -->|Host runtime| kubernetes["Kubernetes"]
```

Terraform definitions will live in `infrastructure/`. Terraform provisions
the cloud foundation; Argo CD manages the application deployments shown in
the delivery view. Specific AWS services and the Kubernetes hosting model
remain decisions for later tickets.

The long-term goal is to make the project deployable to a choice of AWS, Azure,
GCP, or DigitalOcean. The rollout is incremental:

| Stage | Deployment target | Scope |
| --- | --- | --- |
| Local platform | kind | Establish Kubernetes locally before cloud infrastructure. |
| First cloud implementation | AWS | Focus of v0.8.0 — Cloud Infrastructure, using Terraform. |
| Future cloud targets | Azure, GCP, DigitalOcean | Add deployment support through later tickets; no release assigned yet. |

All deployment targets remain planned. Each additional cloud will need its
own infrastructure configuration and validation. See
[ADR-002](../adr/002-terraform-and-cloud-targets.md) for the tool and cloud
rollout decision.

### 3.4 Observability — Planned

Application and platform telemetry feed two data sources. Grafana uses both
to help inspect system behavior.

```mermaid
flowchart TD
  workloads["FastAPI and Kubernetes"] -->|Metrics| prometheus["Prometheus"]
  workloads -->|Collected logs| loki["Loki"]
  prometheus -->|Metrics data| grafana["Grafana"]
  loki -->|Log data| grafana
```

The arrows show telemetry flow. Metrics collection details and log-collection
tooling will be defined in later tickets.

## 4. Architecture Layers

All layers below describe planned capabilities.

### Application

**Planned:** Python, FastAPI, and PostgreSQL.

**Purpose:** Provide a realistic workload for demonstrating platform
engineering and application delivery. The domain is a personal gamified habit
tracker; see [ADR-003](../adr/003-habit-tracker-domain.md).

### Frontend

**Planned:** React and Vite, deployed as a separate service.

**Purpose:** Give the habit tracker a usable interface and give the platform
milestones a realistic multi-service topology to route, deploy, observe, and
roll back independently.

### Build and Delivery

**Planned:** GitHub Actions and GitHub Container Registry.

**Purpose:** Automated validation, builds, and artifact publishing.

### Runtime Platform

**Planned:** Kubernetes and Helm.

**Purpose:** Application orchestration and packaging. Helm will follow working
raw Kubernetes resources.

### GitOps

**Planned:** Argo CD.

**Purpose:** Declarative deployment and desired-state reconciliation.

### Infrastructure

**Planned:** Terraform, with AWS as the first cloud target. Azure, GCP, and
DigitalOcean are future deployment targets.

**Purpose:** Reproducible cloud infrastructure introduced after the local
platform is ready. Additional cloud targets will be implemented incrementally
under the [Terraform and cloud rollout decision](../adr/002-terraform-and-cloud-targets.md).

### Observability

**Planned:** Prometheus, Grafana, and Loki.

**Purpose:** Metrics, dashboards, alerts, and logs for understanding system
behavior and diagnosing problems.

### Reliability and Security

**Planned areas:**

- Health checks.
- Resource limits.
- Autoscaling.
- Backup and restore.
- Security scanning.
- Secrets management.
- Failure testing.
- Incident response.

**Purpose:** Make operational health, recovery, and security practices
observable and verifiable as runtime capabilities are introduced.

## 5. Architecture Evolution

The intended evolution follows the [release roadmap](../roadmap.md):

```text
Bootstrap
    ↓
Application MVP
    ↓
Web Frontend
    ↓
Containers
    ↓
CI
    ↓
Kubernetes
    ↓
Helm
    ↓
GitOps
    ↓
Observability
    ↓
Cloud Infrastructure (Terraform, AWS first)
    ↓
Security and Reliability
    ↓
Production Simulation
```

Azure, GCP, and DigitalOcean deployment support is a longer-term goal beyond
the initial AWS cloud milestone; releases for those targets are not assigned.

Update this architecture documentation as each stage becomes real. Move
capabilities into the current architecture only after their implementation
and relevant validation exist. Record significant decisions in ADRs and keep
the target direction aligned with the evolving roadmap.

## 6. Current Milestone

The current milestone is **v0.1.0 — Application MVP**, consistent with the
[README](../../README.md) and [roadmap](../roadmap.md). The next planned release
milestone is **v0.1.5 — Web Frontend**.
