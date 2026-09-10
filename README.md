# One Serious Project

One Serious Project is a production-style DevOps platform being built
incrementally as a monorepo. It aims to demonstrate professional practices in
application delivery, containers, CI/CD, Kubernetes, GitOps, Infrastructure as
Code, cloud infrastructure, observability, security, reliability, incident
response, and cost awareness.

## Current status

Current milestone: Epic 0 — Bootstrap

The repository is currently being initialized. It contains the initial folder
structure and shared project configuration. Application and platform components
will be introduced in later milestones.

## Planned technology stack

The target stack below is planned; these technologies are not yet implemented:

- Python / FastAPI and PostgreSQL
- Docker, GitHub Actions, and GitHub Container Registry
- kind, Kubernetes, Helm, and Argo CD
- Terraform, with AWS as the first cloud target
- Prometheus, Grafana, and Loki
- k6 and Trivy

Cloud infrastructure will follow a working local platform. The first cloud
implementation will focus on AWS; the long-term goal is to make the project
deployable to a choice of AWS, Azure, GCP, or DigitalOcean. Support for the
additional clouds will be introduced through future tickets.

## Repository structure

Directories reserve space for the planned components and documentation:

```text
one-serious-project/
├── app/                  Application source
├── infrastructure/       Infrastructure as Code
├── kubernetes/           Kubernetes configuration
├── helm/                 Helm charts
├── argocd/               GitOps configuration
├── monitoring/           Observability configuration
├── scripts/              Automation scripts
├── tests/                Test assets
├── docs/                 Architecture and operational documentation
│   ├── roadmap.md
│   ├── development/
│   ├── architecture/
│   ├── adr/
│   ├── runbooks/
│   ├── incidents/
│   └── security/
├── .github/              GitHub project automation and templates
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── Makefile
├── .gitignore
├── .editorconfig
└── LICENSE
```

Empty directories contain `.gitkeep` files so Git can preserve the structure.

## Development approach

The project is intentionally built brick by brick. Planned components will only
be introduced in their appropriate milestones. Setup steps and development
commands will be documented as they are added.

See the [project roadmap](docs/roadmap.md) for planned releases and bootstrap
tickets, and the [development workflow](docs/development/workflow.md) for branch
and pull request practices.

See the [Architecture Overview](docs/architecture/overview.md) for current and
planned states. Accepted architecture decisions cover the
[monorepo strategy](docs/adr/001-monorepo.md) and
[Terraform and cloud targets](docs/adr/002-terraform-and-cloud-targets.md).

With Make installed, list the available commands:

```sh
make help
```

Build, test, and deployment commands have not been configured yet.

## Agent guidance

See [AGENTS.md](AGENTS.md) for repository instructions. [CLAUDE.md](CLAUDE.md)
points to the same guidance.

## License

Licensed under the [MIT License](LICENSE).

