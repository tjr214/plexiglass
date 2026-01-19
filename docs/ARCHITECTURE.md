# PlexiGlass - Application Architecture

**Project**: PlexiGlass  
**Version**: 0.1.0  
**Last Updated**: 2026-01-16  
**Status**: Architecture Design Phase

---

## 🏛️ High-Level Architecture

PlexiGlass follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      TEXTUAL TUI LAYER                      │
│  (Screens, Widgets, Event Handlers, CSS Styling)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                  APPLICATION LOGIC LAYER                     │
│  (Controllers, State Management, Business Logic)            │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                    SERVICE LAYER                            │
│  (Plex API Clients, Server Manager, Undo System)           │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                     DATA LAYER                              │
│  (Configuration, Cache, State Storage)                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
plexiglass/
├── src/
│   └── plexiglass/
│       ├── __init__.py
│       ├── __main__.py                 # Entry point
│       │
│       ├── app/                        # Main application
│       │   ├── __init__.py
│       │   └── plexiglass_app.py       # Main Textual App class
│       │
│       ├── ui/                         # UI Components
│       │   ├── __init__.py
│       │   ├── screens/                # Textual Screens
│       │   │   ├── __init__.py
│       │   │   ├── main_screen.py      # Main dashboard screen
│       │   │   ├── gallery_screen.py   # Gallery mode screen
│       │   │   └── server_select_screen.py
│       │   │
│       │   ├── widgets/                # Custom Widgets
│       │   │   ├── __init__.py
│       │   │   ├── server_card.py      # Server status card
│       │   │   ├── api_demo.py         # API demo widget
│       │   │   ├── code_viewer.py      # Code example viewer
│       │   │   └── undo_button.py      # Undo operation button
│       │   │
│       │   └── styles/                 # CSS Stylesheets
│       │       ├── __init__.py
│       │       ├── main.tcss           # Main styles
│       │       ├── dashboard.tcss      # Dashboard styles
│       │       └── gallery.tcss        # Gallery styles
│       │
│       ├── controllers/                # Application Controllers
│       │   ├── __init__.py
│       │   ├── dashboard_controller.py
│       │   └── gallery_controller.py
│       │
│       ├── services/                   # Business Services
│       │   ├── __init__.py
│       │   ├── plex_service.py         # Plex API wrapper
│       │   ├── server_manager.py       # Multi-server management
│       │   ├── undo_service.py         # Undo/redo functionality
│       │   └── demo_service.py         # Gallery demo execution
│       │
│       ├── models/                     # Data Models
│       │   ├── __init__.py
│       │   ├── server.py               # Server model
│       │   ├── demo.py                 # Demo metadata model
│       │   └── undo_stack.py           # Undo stack model
│       │
│       ├── config/                     # Configuration
│       │   ├── __init__.py
│       │   ├── settings.py             # Application settings
│       │   └── servers.yaml            # Server configurations
│       │
│       ├── gallery/                    # Gallery Mode Demos
│       │   ├── __init__.py
│       │   ├── base_demo.py            # Base demo class
│       │   ├── registry.py             # Demo registry
│       │   │
│       │   ├── server/                 # Server demos
│       │   │   ├── __init__.py
│       │   │   ├── connection_demo.py
│       │   │   └── ...
│       │   │
│       │   ├── library/                # Library demos
│       │   │   ├── __init__.py
│       │   │   └── ...
│       │   │
│       │   ├── media/                  # Media demos
│       │   │   ├── __init__.py
│       │   │   └── ...
│       │   │
│       │   └── [other categories]/
│       │
│       └── utils/                      # Utilities
│           ├── __init__.py
│           ├── logger.py               # Logging utilities
│           └── helpers.py              # Helper functions
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/                           # Unit tests
│   │   ├── test_services/
│   │   ├── test_models/
│   │   └── test_gallery/
│   │
│   └── integration/                    # Integration tests
│       ├── test_ui/
│       └── test_plex_api/
│
├── docs/                               # Documentation
│   ├── LIVING_DOCS.md
│   ├── API_FEATURES_MAP.md
│   ├── ARCHITECTURE.md                 # This file
│   └── TECHNICAL_SPEC.md
│
├── config/                             # Configuration files
│   └── servers.example.yaml
│
└── pyproject.toml
```

---

## 🎯 Core Components

### 1. Main Application (`app/plexiglass_app.py`)

The main Textual application class that:
- Initializes the TUI
- Manages screen routing
- Handles global keybindings
- Coordinates services

```python
class PlexiGlassApp(App):
    BINDINGS = [
        ("d", "switch_mode('dashboard')", "Dashboard"),
        ("g", "switch_mode('gallery')", "Gallery"),
        ("q", "quit", "Quit"),
    ]
    
    def on_mount(self):
        # Load configuration
        # Initialize services
        # Show main screen
        pass
```

### 2. Server Manager (`services/server_manager.py`)

Manages multiple Plex server connections:
- Load server configurations from YAML
- Maintain connection pool
- Switch active server
- Monitor server health
- Cache server information

### 3. Undo Service (`services/undo_service.py`)

Implements undo/redo functionality:
- **Snapshot Pattern**: Capture state before write operations
- **Command Pattern**: Encapsulate operations as reversible commands
- **Stack Management**: Maintain undo/redo stacks
- **State Restoration**: Restore previous states

```python
class UndoService:
    def snapshot(self, operation: str, restore_data: dict):
        """Capture state before operation"""
        
    def undo(self):
        """Restore last snapshot"""
        
    def can_undo(self) -> bool:
        """Check if undo is available"""
```

### 4. Gallery Demo System (`gallery/`)

**Base Demo Class** (`base_demo.py`):
```python
class BaseDemo(ABC):
    category: str
    name: str
    description: str
    is_write_operation: bool
    
    @abstractmethod
    def get_code_example(self) -> str:
        """Return code example"""
    
    @abstractmethod
    async def execute_read(self, server) -> dict:
        """Execute read demonstration"""
    
    @abstractmethod
    async def execute_write(self, server, params: dict) -> dict:
        """Execute write demonstration (with undo)"""
```

**Demo Registry** (`registry.py`):
- Auto-discover all demo classes
- Organize by category
- Provide search/filter
- Track demo status

### 5. Dashboard Controller (`controllers/dashboard_controller.py`)

Manages dashboard functionality:
- Display server status cards
- Show active sessions
- Monitor server health
- Display library statistics
- Real-time updates

### 6. Gallery Controller (`controllers/gallery_controller.py`)

Manages gallery mode:
- Navigate demo categories
- Execute selected demo
- Display results
- Handle write operations with undo
- Show code examples

---

## 🎨 UI Architecture (Textual)

### Screen Hierarchy

```
PlexiGlassApp
├── MainScreen (Dashboard Mode)
│   ├── Header (server selector)
│   ├── ServerGrid (server cards)
│   ├── SessionsPanel (active sessions)
│   └── Footer (keybindings)
│
└── GalleryScreen (Gallery Mode)
    ├── Header (breadcrumb navigation)
    ├── Sidebar (category menu)
    ├── DemoPanel (demo execution area)
    │   ├── DescriptionPanel
    │   ├── CodeViewer
    │   ├── ResultsPanel
    │   └── ActionButtons (Execute, Undo)
    └── Footer (keybindings)
```

### Custom Widgets

1. **ServerCard**: Displays server status with metrics
2. **CategoryMenu**: Hierarchical menu for gallery navigation (implemented)
3. **CodeViewer**: Syntax-highlighted code display (implemented)
4. **DemoResults**: Pretty-printed API results (implemented)
5. **UndoButton**: Contextual undo button with state

### CSS Theming

PlexiGlass will use Textual's CSS system with custom themes:

```css
/* main.tcss */
Screen {
    background: $surface;
}

ServerCard {
    border: solid $primary;
    background: $panel;
    padding: 1 2;
}

.healthy {
    color: $success;
}

.warning {
    color: $warning;
}

.error {
    color: $error;
}
```

---

## 🔄 Data Flow

### Dashboard Mode Flow

```
User Action → MainScreen → DashboardController → ServerManager → PlexService → Plex API
                                                       ↓
                                                    Cache
                                                       ↓
                                              UI Update (reactive)
```

### Gallery Mode Flow (READ)

```
User Selects Demo → GalleryScreen → GalleryController → DemoService
                                                            ↓
                                                      Execute Demo
                                                            ↓
                                                       Plex API
                                                            ↓
                                                   Format Results
                                                            ↓
                                              Display (Code + Results)
```

### Gallery Mode Flow (WRITE with UNDO)

```
User Executes Write → GalleryController → UndoService.snapshot()
                                                ↓
                                          Execute Write
                                                ↓
                                           Plex API
                                                ↓
                                         Store in Stack
                                                ↓
                                        Show Undo Button
                                                ↓
User Clicks Undo → UndoService.undo() → Restore State → Plex API
```

---

## 🔐 Configuration Management

### Server Configuration (`config/servers.yaml`)

```yaml
servers:
  - name: "Home Server"
    url: "http://192.168.1.100:32400"
    token: "${PLEX_TOKEN_HOME}"
    default: true
    
  - name: "Remote Server"
    url: "https://plex.example.com"
    token: "${PLEX_TOKEN_REMOTE}"
    
  - name: "Test Server"
    url: "http://localhost:32400"
    token: "${PLEX_TOKEN_TEST}"
```

### Application Settings

```python
class Settings:
    # UI
    theme: str = "dark"
    refresh_interval: int = 5  # seconds
    
    # Gallery
    show_code_examples: bool = True
    enable_write_operations: bool = True
    confirm_before_write: bool = True
    
    # Performance
    cache_ttl: int = 60  # seconds
    max_undo_stack: int = 50
```

---

## 🧪 Testing Strategy

### TDD Approach for Each Component

1. **🔴 RED**: Write failing test
2. **🟢 GREEN**: Minimal implementation
3. **🔵 REFACTOR**: Improve while tests pass

### Test Coverage Goals

- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Key workflows (gallery flow covered)
- **UI Tests**: Textual's testing framework

### Example Test Structure

```python
# tests/unit/test_services/test_server_manager.py
class TestServerManager:
    def test_load_servers_from_config(self):
        # Test server loading
        
    def test_switch_active_server(self):
        # Test server switching
        
    def test_connection_health_check(self):
        # Test health monitoring
```

---

## 📊 State Management

### Reactive State (Textual's reactive system)

```python
class MainScreen(Screen):
    active_server = reactive(None)
    sessions = reactive([])
    
    def watch_active_server(self, server):
        """Called when active_server changes"""
        self.refresh_data()
```

### Application State

```python
@dataclass
class AppState:
    servers: list[Server]
    active_server: Server | None
    undo_stack: UndoStack
    demo_history: list[DemoExecution]
```

---

## 🚀 Performance Considerations

1. **Async Operations**: Use `async/await` for API calls
2. **Caching**: Cache server responses with TTL
3. **Lazy Loading**: Load gallery demos on-demand
4. **Background Workers**: Use Textual workers for long operations
5. **Connection Pooling**: Reuse Plex API connections

---

## 🔮 Future Extensions

- Plugin system for custom demos
- Export demo results to files
- Scripting mode (non-interactive)
- Remote control via API
- Multi-language support
- Custom themes gallery

---

**Status**: Architecture Design Complete ✅  
**Next Step**: Create Technical Specification
**Ready for**: Implementation with TDD
