# ADR-003: Adopt a Personal Gamified Habit Tracker as the Application Domain

## Status

Accepted — project-owner direction recorded during Application MVP planning.

## Context

The application exists to provide a realistic workload for the platform,
delivery, and reliability milestones rather than to be an
application-development portfolio. Earlier planning settled on a service desk
domain, but no domain code was ever written; only the domain-neutral FastAPI
scaffold from [OSP-005](https://github.com/jddemonteverde/One-Serious-Project/issues/9)
exists in the repository.

The project owner has changed direction to a gamified habit tracker with a
frontend, backend, and database. The domain needs enough behaviour to exercise
persistence, migrations, health checks, structured logging, metrics, load
testing, and incident scenarios, while remaining small enough that application
development does not displace platform work.

## Options Considered

| Option | Summary | Assessment |
| --- | --- | --- |
| Service desk tickets | Ticket CRUD with priority, status, requester, and assignee. | Enterprise-relatable and a close thematic fit with the project's incident-response documentation, but it is another status-field CRUD application. |
| Personal habit tracker | Habits, daily completions, streaks, points, and badges for a single user. | Selected. The completion write path produces genuine derived state rather than field updates. |
| Workplace wellness tracker | The same mechanics scoped to organizations and teams, with leaderboards. | Retains an enterprise framing and supplies multi-tenancy for later security work, at the cost of a larger schema and more application development. |

## Decision

- Model the application as a personal gamified habit tracker.
- Scope gamification to streaks, points, and badges. Levels and leaderboards are
  out of scope.
- Treat habit completions as the source of truth. Streak counters and point
  totals are maintained aggregates that remain recomputable from completions.
- Enforce uniqueness on a habit and completion date so that double-logging is an
  explicit conflict rather than a duplicate record.
- Ship a `users` table with one seeded user in v0.1.0 and defer authentication to
  the Security and Reliability milestone.

## Consequences

### Positive

- Streak and badge evaluation on the completion write path gives the
  observability and reliability milestones real behaviour to instrument, alert
  on, and break, rather than uniform CRUD traffic.
- Derived state that must stay consistent with its source records creates
  realistic correctness and recovery scenarios for later milestones.
- The schema stays small enough that platform work remains the focus.

### Tradeoffs and Operational Consequences

- **The enterprise framing is dropped.** The earlier goal of an application a
  business could use no longer applies. This was an explicit project-owner
  choice made with the workplace-wellness alternative on the table.
- Single-user data gives the Security and Reliability milestone less to
  demonstrate. Tenant data isolation, role-based access control, and per-tenant
  limits are not exercised by this domain.
- Introducing organizations and teams later would require reworking the schema
  and every query, because a tenant identifier added after the fact propagates
  through all tables and access paths.
- Maintained aggregates can drift from the completion records. A recomputation
  path is needed and should be treated as an operational concern.

## Deferred Decisions

Authentication and multi-user support, the badge criteria catalogue beyond the
initial seeded set, aggregate recomputation tooling, and whether the reported
service name remains `one-serious-project-api` once the domain is implemented.

See the [architecture overview](../architecture/overview.md) and
[roadmap](../roadmap.md) for the planned system and milestone sequence.
