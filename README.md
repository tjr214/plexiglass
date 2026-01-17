# PlexiGlass 🎨

> *Where Transparency Meets Functionality*

A colorful **Textual TUI** (Terminal User Interface) application that serves as both a **multi-server Plex dashboard** and a comprehensive **python-plexapi feature gallery**.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Textual](https://img.shields.io/badge/textual-7.3.0-purple.svg)](https://textual.textualize.io/)
[![PlexAPI](https://img.shields.io/badge/plexapi-4.17.2-orange.svg)](https://python-plexapi.readthedocs.io/)
[![Built with uv](https://img.shields.io/badge/built%20with-uv-green.svg)](https://github.com/astral-sh/uv)

---

## 📖 What is PlexiGlass?

PlexiGlass is a **dual-purpose** terminal application designed for:

### 1. 📡 **Production Dashboard**
Monitor and administer **multiple Plex Media Servers** from a beautiful, keyboard-driven terminal interface:
- Real-time server status monitoring
- Active session tracking across all servers  
- Library statistics and health metrics
- Quick access to common admin tasks
- Colorful, intuitive UI with CSS theming

### 2. 🎓 **Developer Gallery & Reference**
A complete, interactive demonstration platform for **every python-plexapi feature**:
- **15 major categories** covering 200+ API features
- **Live code examples** showing actual usage
- **Interactive demos** pulling real data from your servers
- **Safe write testing** with built-in **UNDO** capability
- Perfect for learning, testing, and reference

---

## ✨ Key Features

### Dashboard Mode
- ✅ Multi-server management from single interface
- ✅ Real-time session monitoring
- ✅ Library health and statistics
- ✅ Performance metrics
- ✅ Quick admin actions

### Gallery Mode  
- ✅ Every python-plexapi feature demonstrated
- ✅ Organized hierarchical menu (15 categories)
- ✅ **READ operations**: Safe data pulling
- ✅ **WRITE operations**: Test with undo capability
- ✅ Live code examples
- ✅ Interactive parameter testing
- ✅ Real results from your selected server

### Safety First
- 🔒 **Read-first approach**: Demos default to safe reads
- ↩️ **Undo system**: Every write can be reversed
- ⚠️ **Confirmation prompts**: Optional safety checks
- 📸 **State snapshots**: Automatic backup before writes
- 🎯 **Server selection**: Choose test vs production servers

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.13+** 
- **uv** package manager ([install](https://github.com/astral-sh/uv))
- One or more **Plex Media Servers** with API access

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
# Edit ~/.config/plexiglass/servers.yaml with your Plex server details

# Set environment variables for tokens
export PLEX_TOKEN_HOME="your-plex-token-here"

# Run PlexiGlass from anywhere!
plexiglass
```

#### Option 2: Development Setup

```bash
# Clone repository
git clone <repo-url>
cd plexiglass

# Install dependencies
uv sync --all-extras

# Copy and configure servers
cp config/servers.example.yaml config/servers.yaml
# Edit config/servers.yaml with your Plex server details

# Set environment variables for tokens
export PLEX_TOKEN_HOME="your-plex-token-here"

# Run tests to verify setup
uv run pytest
```

### Running PlexiGlass

```bash
# If installed globally with uv tool:
plexiglass                # Launch the TUI
plexiglass --version      # Show version
plexiglass --help         # Show help
plexiglass --check-config # Verify configuration

# If running in development:
uv run python -m plexiglass            # Standard launch
uv run plexiglass                      # Using CLI entry point

# Development mode with live reload:
uv run textual run --dev src/plexiglass/app/plexiglass_app.py

# With debug console:
uv run textual console
```

---

## 📚 Gallery Categories

PlexiGlass Gallery Mode demonstrates features across **15 major categories**:

| Category | Features | Examples |
|----------|----------|----------|
| 📡 **Server & Connection** | Connection methods, server info, sessions | Direct connect, MyPlex auth, server details |
| 📚 **Library Management** | Sections, search, maintenance | List libraries, scan, refresh metadata |
| 🎬 **Media Operations** | Movies, TV, Music, Photos | Get details, update metadata, artwork |
| 🎮 **Playback & Clients** | Client control, play queues | Play/pause, skip, volume control |
| 📦 **Collections & Playlists** | Organization, curation | Create collections, manage playlists |
| 👥 **Users & Sharing** | User management, permissions | Share libraries, update permissions |
| 👤 **MyPlex Account** | Account, servers, devices | List servers, manage devices |
| ⚙️ **Settings & Preferences** | Server configuration | View/update server settings |
| 🔍 **Search & Discovery** | Search, recommendations | Global search, advanced filters |
| 📱 **Sync & Offline** | Sync management | Create/manage sync items |
| 🔔 **Alerts & Monitoring** | Real-time updates | Activity alerts, timeline events |
| 🔊 **Integrations** | Sonos, devices | Control Sonos, device discovery |
| 🔬 **Media Analysis** | Streams, codecs | Analyze media, optimize |
| 🛠️ **Utilities** | Tools, helpers | Downloads, uploads, conversions |
| 🧪 **Advanced Features** | Power user tools | Batch operations, automation |

---

## 🏗️ Architecture

PlexiGlass follows a **clean, layered architecture**:

```
┌────────────────────┐
│   Textual TUI      │  Screens, Widgets, CSS Styling
├────────────────────┤
│ Application Logic  │  Controllers, State Management
├────────────────────┤
│  Service Layer     │  Plex API, Undo System, Demos
├────────────────────┤
│   Data Layer       │  Configuration, Cache, State
└────────────────────┘
```

### Key Design Patterns
- **MVC**: Clean separation of concerns
- **Command Pattern**: Undo/redo system
- **Factory Pattern**: Demo registration
- **Observer Pattern**: Reactive state (Textual)

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for full details.

---

## 🧪 Development

### TDD Workflow

PlexiGlass follows **Test-Driven Development**:

1. **🔴 RED**: Write failing test first
2. **🟢 GREEN**: Write minimal code to pass
3. **🔵 REFACTOR**: Improve while tests pass

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html

# Watch mode for TDD
uv run pytest-watch

# Specific category
uv run pytest tests/unit/test_services/
```

### Code Quality

```bash
# Lint code
uv run ruff check .

# Auto-fix issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

---

## 📖 Documentation

- **[Living Documentation](docs/LIVING_DOCS.md)** - Complete project overview and status
- **[Architecture](docs/ARCHITECTURE.md)** - Technical architecture and design
- **[API Features Map](docs/API_FEATURES_MAP.md)** - python-plexapi feature mapping
- **[Technical Spec](docs/TECHNICAL_SPEC.md)** - Implementation specifications (Coming Soon)

---

## 🎯 Project Status

### ✅ Completed

- [x] Project foundation and setup
- [x] Architecture design
- [x] python-plexapi feature mapping (200+ features)
- [x] Undo system design
- [x] Multi-server configuration design
- [x] Gallery demo system design
- [x] Testing infrastructure

### 🔄 In Progress

- [ ] Core implementation (Sprints 1-6)
- [ ] Dashboard mode
- [ ] Gallery foundation
- [ ] Demo implementations

See [LIVING_DOCS.md](docs/LIVING_DOCS.md) for detailed sprint planning.

---

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.13.7 |
| Package Manager | uv | 0.9.18 |
| TUI Framework | Textual | 7.3.0 |
| Plex API | PlexAPI | 4.17.2 |
| Testing | pytest | 9.0.2+ |
| Dev Tools | textual-dev | 1.8.0+ |
| Code Quality | ruff | Latest |
| Config | PyYAML | 6.0.0+ |

---

## 🤝 Contributing

PlexiGlass follows strict development practices:

1. ✅ **Write tests first** (TDD Red-Green-Refactor)
2. ✅ **Follow architecture** patterns
3. ✅ **Update documentation** with changes
4. ✅ **Ensure tests pass** (80%+ coverage target)
5. ✅ **Run ruff** before committing
6. ✅ **Maintain undo capability** for write operations

---

## 📝 License

[To be determined]

---

## 🙏 Acknowledgments

- **[python-plexapi](https://github.com/pkkid/python-plexapi)** - The excellent Plex API library
- **[Textual](https://textual.textualize.io/)** - Modern TUI framework
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package manager
- **BMAD Method** - Development methodology

---

## 📧 Contact

**Maintained by**: Tim  
**Powered by**: BMad Master 🧙

---

<div align="center">
  
**PlexiGlass** - *Bringing clarity to your Plex infrastructure* ✨

</div>
