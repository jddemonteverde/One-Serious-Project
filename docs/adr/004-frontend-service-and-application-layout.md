# ADR-004: Introduce a Separate Frontend Service and a Per-Application Layout

## Status

Accepted — project-owner direction recorded during Application MVP planning.

## Context

The habit tracker adopted in [ADR-003](003-habit-tracker-domain.md) needs a user
interface. Until now the application has been an API only, reachable through
`curl` and the interactive documentation FastAPI generates.

Two questions had to be answered together. How should the frontend be built, and
where should it live? The repository previously used `app/` as a single Python
package. The project owner wants `app/` to hold several applications over time,
which makes the layout question structural rather than cosmetic.

This decision extends the monorepo strategy accepted in
[ADR-001](001-monorepo.md); it does not revisit it.

## Options Considered

| Decision | Options | Selected approach |
| --- | --- | --- |
| Frontend technology | HTMX with Jinja templates inside FastAPI; React with Vite as a separate service; Reflex or NiceGUI; Next.js | React with Vite as a separate service. |
| Directory layout | Keep a single top-level application package; place each application under `app/<application>/` with `backend/` and `frontend/` | Per-application directories under `app/`. |

HTMX inside FastAPI would have been the smallest change and would have kept the
stack entirely in Python, but it leaves the project with one deployable and
therefore no realistic multi-service topology to operate. Reflex and NiceGUI
maximise Python at the cost of niche tooling. Next.js adds a Node runtime to
operate in production without adding capability this project needs.

## Decision

- Build the frontend as a React and Vite application, deployed as its own
  service and reverse-proxied to the FastAPI backend.
- Place each application under `app/<application>/` with separate `backend/` and
  `frontend/` directories.
- Rename the backend Python package from `app` to `habit_tracker`. The directory
  `habit-tracker` contains a hyphen and cannot be a Python package, so the
  importable package must live below it; reusing the name `app` there would
  produce an ambiguous `app.main:app` import string.
- Give the Makefile an `APP` variable so commands target an application by name
  and a second application requires no rework.
- Introduce the frontend in its own milestone, `v0.1.5 — Web Frontend`, after the
  Application MVP.

## Consequences

### Positive

- Two deployables give the Kubernetes, Helm, GitOps, and observability
  milestones genuine ingress routing, service discovery, per-service dashboards,
  and independent deployment and rollback.
- Each deployable owns its dependency manifest and will own its own container
  image and CI path.
- The layout supports additional applications without restructuring, and keeps
  each application's components together.
- Python remains in the backend, where it is the stronger choice.

### Tradeoffs and Operational Consequences

- A second toolchain must be installed, built, dependency-scanned, and patched.
  Node and npm become part of the project's supply chain and its security surface.
- Application development work increases, which is the drift AGENTS.md section 1
  warns against. The frontend is scoped to displaying and editing habit data.
- Running the backend requires changing directory into it first, because
  `python -m` resolves packages relative to the working directory.
- Cross-origin configuration is now required for local development, since the
  Vite development server and the API run on different ports.
- Two services mean two failure domains; a frontend that cannot reach its API is
  a new class of incident to document and handle.

## Deferred Decisions

Adding a `pyproject.toml` with an editable install to remove the working-directory
constraint, Dockerfile placement and base images for each deployable, the
production reverse proxy, frontend state management and styling approach, and
whether shared frontend code across future applications warrants extraction.

See the [architecture overview](../architecture/overview.md) and
[roadmap](../roadmap.md) for the planned system and milestone sequence.
