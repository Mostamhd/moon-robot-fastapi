# Alembic Migrations

This directory contains the database migrations for the Moon Robot API project.

## Overview

Alembic is used to manage database schema changes in a controlled and versioned manner. Each migration represents a set of changes to the database schema.

## Current Migrations

1. `1aa54a9deae0` - Initial migration with robot_state, command_history, and obstacles tables
2. `59ae276bf76e` - Update default direction value for robot_state table

## Common Commands

### Apply all pending migrations
```bash
alembic upgrade head
```

### Create a new migration
```bash
alembic revision -m "Description of changes"
```

### Create a new migration with autogenerate
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Downgrade to a previous version
```bash
alembic downgrade -1  # Downgrade one revision
alembic downgrade base  # Downgrade to base
```

### Check current revision
```bash
alembic current
```

### View migration history
```bash
alembic history
```

## Workflow

1. Make changes to the SQLAlchemy models in `src/models/`
2. Generate a new migration with `alembic revision --autogenerate -m "Description"`
3. Review the generated migration file in `alembic/versions/`
4. Apply the migration with `alembic upgrade head`
