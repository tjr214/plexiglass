# PlexiGlass - Living Documentation

**Project**: PlexiGlass  
**Version**: 0.1.0  
**Last Updated**: 2026-01-17  
**Status**: Sprint 2 Dashboard Mode Complete ✅

---

## 📋 Project Overview

**PlexiGlass** is a colorful Textual TUI (Terminal User Interface) application that serves dual purposes:

1. **Multi-Server Plex Dashboard**: Monitor and admin multiple Plex Media Servers from a beautiful terminal interface
2. **python-plexapi Feature Gallery**: Complete demonstration platform for every python-plexapi feature, serving as both a functional tool and developer reference

### The Vision

PlexiGlass provides transparency and clarity (like glass) into your Plex infrastructure while serving as a living, interactive gallery of API capabilities. It's designed for both production use (dashboard/admin) and developer education (feature gallery with working examples).

### Purpose

- **For Plex Admins**: Centralized dashboard to monitor and manage multiple Plex servers
- **For Developers**: Interactive reference for learning and testing python-plexapi features
- **For Teams**: Shared knowledge base demonstrating API capabilities with live examples

---

## 🎨 Key Features

### 1. Dashboard Mode

- Multi-server status monitoring
- Active session tracking
- Library statistics and health
- Real-time updates
- Server performance metrics
- Quick admin actions

### 2. Gallery Mode

- **15 Major Categories** covering every python-plexapi feature
- **Interactive Demos** with live code examples
- **READ Operations**: Pull data safely from any server
- **WRITE Operations**: Test modifications with **built-in UNDO**
- **Hierarchical Navigation**: Organized menu system
- **Code Examples**: See the actual python-plexapi code
- **Live Results**: Real data from your selected server

### 3. Safety Features

- **Read-First Approach**: All demos default to safe READ operations
- **Undo System**: Every write operation can be undone
- **Confirmation Prompts**: Optional confirmations before write operations
- **State Snapshots**: Automatic state capture before modifications
- **Server Selection**: Test writes on designated test servers

---

## 🏗️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Language** | Python | 3.13.7 |
| **Package Manager** | uv | 0.9.18 |
| **TUI Framework** | Textual | 7.3.0 |
| **Plex API** | PlexAPI | 4.17.2 |
| **Testing** | pytest | 9.0.2 |
| **Async Testing** | pytest-asyncio | 1.3.0 |
| **Mocking** | pytest-mock | 3.15.1 |
| **Dev Tools** | textual-dev | 1.8.0 |
| **Code Quality** | ruff | Latest |
| **Config** | PyYAML | 6.0.0+ |

---

## 📂 Project Structure

```
plexiglass/
├── src/plexiglass/
│   ├── app/                    # Main Textual application
│   ├── ui/                     # Screens, widgets, CSS styles
│   │   ├── screens/            # Dashboard, Gallery, Server Select
│   │   ├── widgets/            # Custom TUI components
│   │   └── styles/             # Textual CSS theming
│   ├── controllers/            # Application logic
│   ├── services/               # Business services (Plex, Undo, etc.)
│   ├── models/                 # Data models
│   ├── config/                 # Configuration management
│   ├── gallery/                # Gallery demo implementations
│   │   ├── server/             # Server & connection demos
│   │   ├── library/            # Library management demos
│   │   ├── media/              # Media operations demos
│   │   └── [13 more categories]
│   └── utils/                  # Utilities & helpers
│
├── tests/
│   ├── unit/                   # Unit tests (TDD)
│   └── integration/            # Integration tests
│
├── docs/
│   ├── LIVING_DOCS.md          # This file
│   ├── ARCHITECTURE.md         # Technical architecture
│   ├── API_FEATURES_MAP.md     # python-plexapi feature mapping
│   └── TECHNICAL_SPEC.md       # Implementation specifications
│
├── config/
│   └── servers.example.yaml    # Server configuration template
│
└── pyproject.toml              # Project configuration
```

---

## 🎯 Gallery Mode Organization

### 15 Feature Categories

1. 📡 **Server & Connection** - Connection methods, server info, sessions
2. 📚 **Library Management** - Sections, search, statistics, maintenance
3. 🎬 **Media Operations** - Movies, TV, Music, Photos
4. 🎮 **Playback & Clients** - Client control, play queues
5. 📦 **Collections & Playlists** - Organization and curation
6. 👥 **Users & Sharing** - User management, permissions
7. 👤 **MyPlex Account** - Account details, servers, devices
8. ⚙️ **Settings & Preferences** - Server configuration
9. 🔍 **Search & Discovery** - Global search, recommendations
10. 📱 **Sync & Offline** - Sync management
11. 🔔 **Alerts & Monitoring** - Real-time notifications
12. 🔊 **Integrations** - Sonos and other devices
13. 🔬 **Media Analysis** - Streams, codecs, optimization
14. 🛠️ **Utilities** - Downloads, uploads, tools
15. 🧪 **Advanced Features** - Power user capabilities

Each category contains:
- **Purpose**: What it does and why
- **Code Examples**: Actual python-plexapi code
- **Live Demos**: Execute against real server
- **Interactive Parameters**: Modify and re-run
- **Undo Capability**: For write operations

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

# Run specific category
uv run pytest tests/unit/test_services/

# Run with verbose output
uv run pytest -v

# Watch mode for TDD
uv run pytest-watch
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

### Running PlexiGlass

```bash
# Standard launch
uv run python -m plexiglass

# With Textual dev tools
uv run textual run --dev src/plexiglass/app/plexiglass_app.py

# Console mode (for debugging)
uv run textual console
```

---

## 🔐 Configuration

### Server Configuration (`config/servers.yaml`)

```yaml
servers:
  - name: "Production Server"
    url: "http://192.168.1.100:32400"
    token: "${PLEX_TOKEN_PROD}"
    default: true
    read_only: false  # Allow write operations
    
  - name: "Test Server"
    url: "http://localhost:32400"
    token: "${PLEX_TOKEN_TEST}"
    read_only: false  # Safe for testing writes
    
  - name: "Friend's Server"
    url: "https://plex.friend.com"
    token: "${PLEX_TOKEN_FRIEND}"
    read_only: true   # Read-only access
```

### Environment Variables

```bash
# Plex tokens (keep secret!)
export PLEX_TOKEN_PROD="your-production-token"
export PLEX_TOKEN_TEST="your-test-token"
export PLEX_TOKEN_FRIEND="your-friend-token"

# Optional: PlexiGlass settings
export PLEXIGLASS_THEME="dark"
export PLEXIGLASS_REFRESH_INTERVAL="5"
```

---

## 🏗️ Architecture Highlights

### Layered Architecture

```
┌──────────────────┐
│   Textual TUI    │  Screens, Widgets, CSS
├──────────────────┤
│ Application Logic│  Controllers, State
├──────────────────┤
│  Service Layer   │  Plex API, Undo System
├──────────────────┤
│   Data Layer     │  Config, Cache, State
└──────────────────┘
```

### Key Design Patterns

- **MVC Pattern**: Separation of UI, logic, and data
- **Command Pattern**: Undo/redo system
- **Factory Pattern**: Demo registration and discovery
- **Observer Pattern**: Reactive state updates (Textual reactive)
- **Repository Pattern**: Server configuration management

### Undo System

```python
# Snapshot before write
undo_service.snapshot("update_metadata", {
    "item_id": 123,
    "original_title": "Old Title",
    "original_rating": 8.5
})

# Execute write operation
item.edit_title("New Title")

# Undo if needed
undo_service.undo()  # Restores "Old Title"
```

---

## ✅ Implementation Status

### ✅ Phase 1: Project Foundation (COMPLETE)

- [x] Project renamed to PlexiGlass
- [x] Python 3.13.7 configured
- [x] uv package manager setup
- [x] Textual 7.3.0 installed
- [x] PlexAPI 4.17.2 installed
- [x] PyYAML for configuration
- [x] Testing infrastructure (pytest, asyncio, mock, coverage)
- [x] Textual dev tools installed
- [x] Code quality tools (ruff)
- [x] Project structure designed
- [x] Sample tests passing (100% coverage)

### ✅ Phase 2: Planning & Architecture (COMPLETE)

- [x] Vision and requirements defined
- [x] python-plexapi features mapped (15 categories, 200+ features)
- [x] Application architecture designed
- [x] Component structure planned
- [x] UI/UX hierarchy defined
- [x] Undo system designed
- [x] Multi-server configuration planned
- [x] Gallery demo system designed
- [x] Testing strategy defined
- [x] Documentation structure created
- [x] CLI entry point configured
- [x] System-wide installation supported (uv tool install)
- [x] Placeholder TUI app created and tested

### 🔄 Phase 3: Core Implementation (IN PROGRESS)

#### Sprint 1: Foundation (COMPLETE)
- [x] Server configuration system
- [x] Server manager service
- [x] Basic Textual app structure
- [x] Main screen layout
- [x] Server card widget
- [x] Configuration loader

#### Sprint 2: Dashboard Mode (COMPLETE)
- [x] Server status dashboard cards (status, sessions, now playing)
- [x] Dashboard summary totals (servers, connected, sessions)
- [x] Dashboard summary library stats (libraries, items)
- [x] Real-time updates (refresh interval loop)
- [x] Active sessions display (session details panel)
- [x] Server health monitoring (last update timestamp)
- [x] Quick actions menu with buttons
- [x] Command prompt modal (input, history, output, ESC dismiss, ':' shortcut)
- [x] Command prompt suggestions (grouped, help text, pagination)
- [x] Command prompt commands: refresh/connect/disconnect/edit_config/list_servers/list_libraries/quit
- [x] Command prompt partial-match + clickable command list
- [x] Config setup flow (blocking prompt + multi-server builder)
- [x] Config defaults (user-local path, full settings write, validation)
- [x] Edit config flow (reuse builder + load existing config)
- [x] Dashboard CSS layout and theming

#### Sprint 3: Gallery Foundation
- [ ] Gallery screen layout
- [ ] Category menu navigation
- [ ] Base demo class
- [ ] Demo registry system
- [ ] Code viewer widget
- [ ] Results display widget

#### Sprint 4: Undo System
- [ ] Undo service implementation
- [ ] Snapshot system
- [ ] Undo stack management
- [ ] Undo button widget
- [ ] State restoration
- [ ] Integration tests

#### Sprint 5: Gallery Demos (15 sprints - one per category)
- [ ] Server & Connection demos
- [ ] Library Management demos
- [ ] Media Operations demos (Movies, TV, Music, Photos)
- [ ] Playback & Clients demos
- [ ] Collections & Playlists demos
- [ ] Users & Sharing demos
- [ ] MyPlex Account demos
- [ ] Settings demos
- [ ] Search & Discovery demos
- [ ] Sync demos
- [ ] Alerts & Monitoring demos
- [ ] Integrations demos
- [ ] Media Analysis demos
- [ ] Utilities demos
- [ ] Advanced Features demos

#### Sprint 6: Polish & Performance
- [ ] CSS theming
- [ ] Performance optimization
- [ ] Error handling
- [ ] Loading states
- [ ] Help system
- [ ] Keyboard shortcuts

---

## 🎯 Success Criteria

### For Admins
- ✅ Monitor multiple servers from single TUI
- ✅ View active sessions across all servers
- ✅ Quick access to common admin tasks
- ✅ Real-time updates (< 5s refresh)
- ✅ Intuitive keyboard navigation

### For Developers
- ✅ Every python-plexapi feature demonstrated
- ✅ Working code examples for each feature
- ✅ Safe testing environment with undo
- ✅ Clear organization by category
- ✅ Copy-pasteable code examples

### For Project
- ✅ 80%+ test coverage
- ✅ All tests passing
- ✅ TDD workflow maintained
- ✅ Living documentation updated
- ✅ Clean, maintainable code

---

## 📚 Documentation Links

- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **API Features**: See [API_FEATURES_MAP.md](./API_FEATURES_MAP.md)
- **Technical Spec**: See [TECHNICAL_SPEC.md](./TECHNICAL_SPEC.md) (Coming Soon)

---

## 🚀 Quick Start (When Ready)

### Installation

#### Option 1: Install as System-Wide Tool (Recommended)

```bash
# Install PlexiGlass globally with uv
uv tool install plexiglass

# Or install from local directory
cd /path/to/plexiglass
uv tool install .

# Configure servers
mkdir -p ~/.config/plexiglass
cp config/servers.example.yaml ~/.config/plexiglass/servers.yaml
# Edit ~/.config/plexiglass/servers.yaml

# Set environment variables
export PLEX_TOKEN_HOME="your-plex-token"

# Run from anywhere!
plexiglass
```

#### Option 2: Development Setup

```bash
# Clone and setup
git clone <repo>
cd plexiglass
uv sync --all-extras

# Configure servers
cp config/servers.example.yaml config/servers.yaml
# Edit config/servers.yaml with your server details

# Run tests
uv run pytest

# Launch PlexiGlass
uv run python -m plexiglass
# OR
uv run plexiglass
```

### CLI Commands

```bash
plexiglass              # Launch TUI
plexiglass --version    # Show version
plexiglass --help       # Show help
plexiglass --check-config  # Verify configuration
```

---

## 📝 Development Notes

- All dependencies use `>=` operator for flexibility
- Tests configured with async support
- Textual dev tools included for live development
- Ruff configured for Python 3.13 best practices
- Living Documentation updated after each sprint
- TDD Red-Green-Refactor cycle enforced
- Code reviews before sprint completion

---

## 🤝 Contribution Guidelines (Future)

1. Write tests first (TDD)
2. Follow existing architecture
3. Update Living Documentation
4. Ensure all tests pass
5. Run ruff before committing
6. Keep undo functionality for writes

---

**Document maintained by**: BMad Master 🧙  
**For**: Tim  
**Project**: PlexiGlass - Where Transparency Meets Functionality ✨
