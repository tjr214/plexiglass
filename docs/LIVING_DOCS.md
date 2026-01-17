# Plex Test - Living Documentation

**Project**: Plex Test  
**Version**: 0.1.0  
**Last Updated**: 2026-01-16  
**Status**: Initial Setup Complete ✅

---

## 📋 Project Overview

A Python project using `python-plexapi` (v4.17.2) for Plex Media Server automation and management.

### Purpose
To be defined based on specific use case requirements.

### Tech Stack
- **Python**: 3.13.7
- **Package Manager**: uv (0.9.18)
- **Main Library**: PlexAPI 4.17.2
- **Testing**: pytest, pytest-cov, pytest-mock
- **Code Quality**: ruff

---

## 🏗️ Project Structure

```
plex-test/
├── src/
│   └── plex_test/          # Main application code
│       ├── __init__.py
│       └── sample.py       # Sample module for TDD demonstration
├── tests/                  # All tests (unit + integration)
│   ├── __init__.py
│   └── conftest.py        # Pytest configuration and fixtures
├── docs/                   # Living documentation
│   └── LIVING_DOCS.md     # This file
├── pyproject.toml         # Project configuration and dependencies
├── .python-version        # Python version (3.13.7)
└── README.md              # Project readme
```

---

## 🔄 Development Workflow

### TDD Red-Green-Refactor Cycle

This project follows **Test-Driven Development (TDD)** principles:

1. **🔴 RED**: Write a failing test first
2. **🟢 GREEN**: Write minimal code to make the test pass
3. **🔵 REFACTOR**: Improve code while keeping tests passing

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_sample.py

# Run with verbose output
uv run pytest -v
```

### Code Quality

```bash
# Run linter
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

---

## 📚 PlexAPI Quick Reference

### Connection to Plex Server

```python
from plexapi.server import PlexServer

# Direct connection
plex = PlexServer('http://localhost:32400', 'YOUR_TOKEN')

# Using PlexAccount
from plexapi.myplex import MyPlexAccount
account = MyPlexAccount('username', 'password')
plex = account.resource('ServerName').connect()
```

### Common Operations

```python
# Get all libraries
libraries = plex.library.sections()

# Get specific library
movies = plex.library.section('Movies')

# Search
results = movies.search('The Matrix')

# Get recently added
recent = movies.recentlyAdded()
```

---

## ✅ Implementation Status

### ✅ Phase 1: Project Initialization (COMPLETE)
- [x] Python 3.13.7 configured
- [x] uv package manager setup
- [x] pyproject.toml created with PlexAPI 4.17.2
- [x] Testing infrastructure (pytest, coverage, mocking)
- [x] Code quality tools (ruff)
- [x] Project structure (src/, tests/, docs/)
- [x] Sample module and test setup
- [x] Living Documentation initialized

### 🔄 Phase 2: Requirements Gathering (NEXT)
- [ ] Define specific use case for PlexAPI
- [ ] Identify key features to implement
- [ ] Design architecture
- [ ] Plan TDD test scenarios

---

## 🎯 Next Steps

1. **Define Project Goals**: Determine what to build with PlexAPI
2. **Plan Features**: Break down into testable components
3. **TDD Implementation**: Build features following Red-Green-Refactor
4. **Documentation**: Keep this Living Doc updated with each implementation

---

## 📝 Notes

- All dependencies are pinned with `>=` operator for flexibility
- Tests are configured to fail if coverage drops below target
- Ruff is configured for Python 3.13 with modern best practices
- Living Documentation should be updated after each significant change

---

**Document maintained by**: BMad Master 🧙  
**For**: Tim
