# DevOps Engineer Interview Assignment: Broken Production Deploy

**Time Limit:** 2 hours  

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
- **Phase 1:** Fix docker-compose.yml end goal should be that application is running fine locally using `docker compose up -d` all the application endpoints should be reachable on `http://localhost/<endpoint>`
- **Phase 2:** Fix Ansible present in infrastructure folder, end goal here is to deploy this complete project on a linux machine using Ansible
- **Phase 3:** Fix CI/CD any new commit into this github repo should trigger CI/CD pipeline and should be able to test, build and deploy application
- **Phase 4:** Fix monitoring script — log parsing, error rate, process safety
- **Phase 5:** Git forensics — identify red herrings vs. real bugs (do it at last)

## Evaluation Criteria
| Category | Weight |
|----------|--------|
| Docker Compose | 25% |
| Ansible | 25% |
| GitHub Actions | 25% |
| Bash Monitoring | 15% |
| Git Forensics | 10% |

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
