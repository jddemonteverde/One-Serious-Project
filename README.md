# One Serious Project

One Serious Project is a production-style DevOps platform being built
incrementally as a monorepo. It aims to demonstrate professional practices in
application delivery, containers, CI/CD, Kubernetes, GitOps, Infrastructure as
Code, cloud infrastructure, observability, security, reliability, incident
response, and cost awareness.

## Current status

Current milestone: v0.1.0 — Application MVP

Epic 0 — Bootstrap is complete. The application is a personal gamified habit
tracker: habits, daily completions, streaks, points, and badges. It is
deliberately small, because its purpose is to provide a realistic workload for
the platform milestones.

The backend serves a habits API with full CRUD and request validation, and
reads its configuration from environment variables. The frontend is currently a
shell that displays the backend's service status.

Habits are stored in PostgreSQL and survive a restart, and the schema is
managed with Alembic migrations. Completions, streaks, points, badges, health
checks, structured logging, metrics, and automated tests are the remaining
Application MVP tickets, and the frontend has no habit features yet. No
container, CI pipeline, or platform component is implemented yet.

## Technology stack

Implemented:

- Python 3.12 and FastAPI, run locally with Uvicorn
- PostgreSQL 16, accessed with SQLAlchemy and migrated with Alembic
- React 19 and Vite 8 with TypeScript, run locally with the Vite dev server

Planned; not yet implemented:

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

`app/` holds applications, each in its own directory with separate backend and
frontend components. The remaining directories reserve space for the planned
platform components and documentation:

```text
one-serious-project/
├── app/                          Applications
│   └── habit-tracker/
│       ├── backend/              FastAPI service
│       │   ├── habit_tracker/    Python package
│       │   │   ├── __main__.py   Local server entry point
│       │   │   ├── main.py       FastAPI application and routes
│       │   │   ├── config.py     Environment-driven settings
│       │   │   ├── database.py   Engine, sessions, and startup check
│       │   │   └── models.py     SQLAlchemy models
│       │   ├── migrations/       Alembic environment and revisions
│       │   │   └── versions/
│       │   ├── alembic.ini       Alembic configuration (no credentials)
│       │   └── requirements.txt  Pinned runtime dependencies
│       └── frontend/             React application
│           ├── src/
│           │   ├── App.tsx       Application shell
│           │   └── api.ts        Backend API client
│           ├── vite.config.ts    Dev server and API proxy
│           └── package.json      Pinned frontend dependencies
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
The directory `habit-tracker` cannot itself be a Python package because of the
hyphen, so the importable package `habit_tracker` lives inside `backend/`. See
[ADR-004](docs/adr/004-frontend-service-and-application-layout.md).

## Local development

### Prerequisites

- Python 3.12
- PostgreSQL 16
- Node.js 22
- Make

### Set up the database

Install and start PostgreSQL, then create the role and database the service
expects:

```sh
brew install postgresql@16
brew services start postgresql@16
export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"

createuser --superuser osp
createdb --owner=osp osp_habit_tracker
```

The Homebrew formula is keg-only, so its binaries are not on `PATH` by default;
add the `export` line to your shell profile to keep `psql` available.

This creates an empty database. The schema is applied with migrations after
the backend is installed; see [Apply database migrations](#apply-database-migrations).

### Install the backend

Create the application's virtual environment in
`app/habit-tracker/backend/.venv` and install its pinned dependencies:

```sh
make install
```

Commands act on the `habit-tracker` application by default. Select another
application with `APP=<name>`, and override the interpreter with `PYTHON=<path>`
if `python3.12` is installed elsewhere:

```sh
make install PYTHON=/path/to/python3.12
```

### Apply database migrations

The schema is version controlled with Alembic. Bring a new or out-of-date
database up to the current revision with:

```sh
make migrate
```

Migrations read the same `DB_*` variables as the service (see
[Backend configuration](#backend-configuration)), so the same overrides apply.
The service does not create or migrate tables itself: if you start it against
an unmigrated database it logs an error naming this command and returns `503`
from the habits endpoints until the schema is applied.

If your database was created by an earlier version of the service, which built
the tables at startup, the tables already match the initial revision. Record
that without touching them:

```sh
cd app/habit-tracker/backend && .venv/bin/alembic stamp head
```

See [Database migrations](#database-migrations) for the full workflow.

### Run the backend

```sh
make run
```

The API listens on `http://127.0.0.1:8000` unless you override the
configuration below.

### Verify the backend

```sh
curl http://localhost:8000/
```

Expected response:

```json
{"service":"one-serious-project-api","status":"running","environment":"local"}
```

Interactive API documentation is generated by FastAPI at
`http://localhost:8000/docs`.

### Backend configuration

The backend reads all configuration from environment variables. Defaults
are development-safe, and no environment-specific value is hardcoded. An
unusable value stops startup with an explicit error rather than falling back
to a default.

| Variable | Default | Description |
| --- | --- | --- |
| `APP_ENV` | `local` | Environment name reported by the service. |
| `APP_HOST` | `127.0.0.1` | Address the server binds to. Container and cluster runtimes will set `0.0.0.0`. |
| `APP_PORT` | `8000` | TCP port the server listens on. Must be between 1 and 65535. |
| `LOG_LEVEL` | `INFO` | Root log level. One of `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG`. |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated origins permitted to call the API directly. Empty disables cross-origin requests. |
| `DB_HOST` | `127.0.0.1` | PostgreSQL host. |
| `DB_PORT` | `5432` | PostgreSQL port. |
| `DB_NAME` | `osp_habit_tracker` | Database name. |
| `DB_USER` | `osp` | Database role. |
| `DB_PASSWORD` | empty | Database password. Empty suits a local trust-authenticated server; **any deployed environment must set it.** |

Example:

```sh
APP_ENV=staging APP_PORT=9001 LOG_LEVEL=DEBUG make run
```

Database credentials are read from the environment and are never committed. A
`Settings` object renders its password as `***`, so logging one cannot leak it.
When the database is unreachable the service still starts and returns `503` from
endpoints that need it, which keeps an outage distinguishable from a crash.

### Database migrations

Schema changes are made through Alembic revisions in
`app/habit-tracker/backend/migrations/versions/`, never by hand-run SQL. The
Alembic environment builds its connection from the `DB_*` variables through the
service's own settings, so `alembic.ini` holds no URL or credentials.

| Command | Purpose |
| --- | --- |
| `make migrate` | Apply every pending revision (`alembic upgrade head`). |
| `make migrate-rollback` | Revert the most recent revision (`alembic downgrade -1`). |
| `make migration MESSAGE="..."` | Generate a revision from model changes (`alembic revision --autogenerate`). |

To change the schema:

1. Edit the models in `habit_tracker/models.py`.
2. Run `make migration MESSAGE="add completions table"` against a database
   that is at the current head. Autogenerate diffs the models against the live
   schema, so an out-of-date database produces a wrong revision.
3. Review the generated file. Autogenerate misses some changes, such as
   renames, and never writes data migrations.
4. Run `make migrate`, then `make migrate-rollback` and `make migrate` again,
   to prove the revision applies and reverses cleanly.
5. Commit the revision with the model change.

Reverting drops whatever the revision created, including its data. Run
`make migrate-rollback` against a shared database only when you mean to.

For other Alembic commands, run the CLI from the backend directory:
`.venv/bin/alembic history`, `.venv/bin/alembic current`, and
`.venv/bin/alembic upgrade head --sql` to print the SQL without applying it.

### Habits API

A habit is something to do on a recurring cadence, worth points when completed.
Completions, streaks, points, and badges arrive in later tickets.

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/habits` | Create a habit. Returns `201`. |
| `GET` | `/habits` | List every habit, oldest first. |
| `GET` | `/habits/{id}` | Return one habit. |
| `PUT` | `/habits/{id}` | Replace a habit's fields. |
| `DELETE` | `/habits/{id}` | Delete a habit. Returns `204`. |

Habit fields:

| Field | Required | Default | Rules |
| --- | --- | --- | --- |
| `name` | Yes | — | 1 to 100 characters, not blank once trimmed. |
| `description` | No | `null` | Up to 500 characters. A blank value is stored as `null`. |
| `cadence` | No | `daily` | One of `daily` or `weekly`. |
| `points_per_completion` | No | `10` | Between 1 and 100. |
| `is_archived` | No | `false` | Hides a habit without deleting it. |

`id` and `created_at` are assigned by the server. `PUT` is a full replacement,
so a field the client omits returns to its default rather than keeping its
previous value. Unknown identifiers return `404`; invalid input returns `422`
with the offending field named.

```sh
curl -X POST http://localhost:8000/habits \
  -H 'Content-Type: application/json' \
  -d '{"name":"Read 20 pages","cadence":"daily","points_per_completion":10}'
```

Habits are stored in PostgreSQL and survive a restart. Every habit belongs to a
single seeded user; authentication arrives in a later milestone.

## Frontend development

The frontend is a separate application in `app/habit-tracker/frontend/`. It is
currently an application shell that reads and displays the backend's service
status; habit features arrive in later tickets.

### Install and run the frontend

```sh
make frontend-install
make frontend-dev
```

The dev server listens on `http://127.0.0.1:5173`. Run the backend in another
terminal with `make run`, or the frontend will show a visible error and a retry
button rather than a blank page.

### Build and lint

```sh
make frontend-build
make frontend-lint
```

### Frontend configuration

By default the browser calls the API through the relative path `/api`, which
the dev server proxies to the backend. That keeps requests same-origin, so no
cross-origin configuration is needed for local work.

| Variable | Default | Description |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `/api` | Base URL the browser uses for API calls. Set an absolute URL to bypass the proxy, which then requires the backend's `CORS_ALLOWED_ORIGINS` to include this origin. |
| `BACKEND_URL` | `http://127.0.0.1:8000` | Backend that the dev server proxies `/api` to. |
| `FRONTEND_PORT` | `5173` | Port the dev server listens on. |

See `app/habit-tracker/frontend/.env.example`. Copy it to `.env.local` to
override any value; `.env.local` is not committed.

## Development approach

The project is intentionally built brick by brick. Planned components will only
be introduced in their appropriate milestones. Setup steps and development
commands are documented as they are added.

See the [project roadmap](docs/roadmap.md) for planned releases and bootstrap
tickets, and the [development workflow](docs/development/workflow.md) for branch
and pull request practices.

See the [Architecture Overview](docs/architecture/overview.md) for current and
planned states. Accepted architecture decisions cover the
[monorepo strategy](docs/adr/001-monorepo.md),
[Terraform and cloud targets](docs/adr/002-terraform-and-cloud-targets.md),
the [habit tracker domain](docs/adr/003-habit-tracker-domain.md), and the
[frontend service and application layout](docs/adr/004-frontend-service-and-application-layout.md).

With Make installed, list the available commands:

```sh
make help
```

Container, CI, and deployment commands have not been configured yet. `make test`
arrives with the automated test ticket. The backend has no linter configured;
`make frontend-lint` covers the frontend only.

## Agent guidance

See [AGENTS.md](AGENTS.md) for repository instructions. [CLAUDE.md](CLAUDE.md)
points to the same guidance.

## License

Licensed under the [MIT License](LICENSE).

