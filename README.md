# DevOps Engineer Interview Assignment: Broken Production Deploy

**Time Limit:** 2 hours  
**Difficulty:** Maximum (Expert Level)

## Scenario
You are a DevOps engineer on-call. Production deployment of a microservices application is completely broken. The CI/CD pipeline fails, containers won't start, and the monitoring system isn't working.

Your mission: diagnose, fix, and harden the entire deployment pipeline in 2 hours.

The repository contains a git history with multiple commits. Some commits introduced real bugs, while others are red herrings (cosmetic changes with no functional impact). You must use git forensics to understand what broke.

## Architecture
```
                    ┌─────────────┐
                    │   nginx     │
                    │  :80        │
                    └──┬─────┬────┘
                       │     │
              /users   │     │  /orders
                       │     │
              ┌────────▼──┐  ┌─▼──────────────┐
              │user-service│  │order-service   │
              │   :8000   │  │    :8080       │
              └──┬─────────┘  └─┬──────────────┘
                 │             │
            ┌────▼──┐      ┌───▼──┐
            │ redis │      │  db  │
            │ :6379 │      │:5432 │
            └───────┘      └──────┘
```

## What You Need to Do
- **Phase 1:** Git forensics — identify red herrings vs. real bugs
- **Phase 2:** Fix docker-compose.yml — env vars, ports, healthchecks, security
- **Phase 3:** Fix Ansible — inventory, modules, vault, firewall
- **Phase 4:** Fix CI/CD — tests, multi-arch builds, secrets, approval gates
- **Phase 5:** Fix monitoring script — log parsing, error rate, process safety

## Evaluation Criteria
| Category | Weight |
|----------|--------|
| Git Forensics | 15% |
| Docker Compose | 25% |
| Ansible | 25% |
| GitHub Actions | 20% |
| Bash Monitoring | 15% |

## Submission
1. Commit each fix separately with clear messages
2. Final state should be a working deployment

## Rules
- 2 hours total
- Use any resources available
- Each fix should be committed separately

## API Endpoints

### User Service
- `GET /users` - List all users
- `GET /users/<id>` - Get user by ID
- `GET /health` - Health check
- `GET /cache/stats` - Cache statistics

### Order Service
- `POST /orders` - Create order
- `GET /orders/user/<id>` - Get orders by user
- `GET /health` - Health check
