# PlexiGlass - python-plexapi Features Map

This document maps out all the features of python-plexapi that will be demonstrated in PlexiGlass Gallery Mode.

**Last Updated**: 2026-01-16  
**python-plexapi Version**: 4.17.2

---

## 📚 Module Organization

PlexiGlass Gallery Mode will organize python-plexapi features into the following categories:

### 1. **Server & Connection**
*Module: `plexapi.server`, `plexapi.myplex`, `plexapi.config`*

**READ Operations:**
- Connect to Plex Server (direct and via MyPlex)
- Get server information (version, platform, etc.)
- List available libraries
- Get server preferences and settings
- Check server capabilities
- View server identity
- Get transcoder sessions
- Get active sessions

**WRITE Operations (with UNDO):**
- Update server settings
- Refresh library sections
- Empty trash
- Optimize database
- Clean bundles

---

### 2. **Library Management**
*Module: `plexapi.library`*

**READ Operations:**
- List all library sections
- Get library section details
- Browse library contents
- Get recently added media
- Get on deck items
- Search library (by title, year, genre, etc.)
- Get library filters
- Get library sorts
- View library statistics

**WRITE Operations (with UNDO):**
- Scan library
- Refresh library metadata
- Update library section settings
- Delete library section
- Add library section
- Merge media items
- Split media items
- Match/unmatch media

---

### 3. **Media Operations**

#### 3.1 **Movies**
*Module: `plexapi.video`*

**READ Operations:**
- List all movies
- Get movie details (title, year, rating, etc.)
- Get movie metadata (actors, directors, etc.)
- View posters and art
- Get subtitles and audio tracks
- View movie collections
- Get similar movies
- Get movie reviews/ratings

**WRITE Operations (with UNDO):**
- Update movie metadata
- Rate movie
- Mark as watched/unwatched
- Add to collection
- Remove from collection
- Edit posters/artwork
- Download subtitles
- Delete movie

#### 3.2 **TV Shows**
*Module: `plexapi.video`*

**READ Operations:**
- List all TV shows
- Get show details
- List seasons
- List episodes
- Get episode metadata
- Track watch progress
- Get next up episodes

**WRITE Operations (with UNDO):**
- Update show/episode metadata
- Mark episodes watched/unwatched
- Rate shows/episodes
- Edit posters/artwork
- Delete shows/seasons/episodes

#### 3.3 **Music**
*Module: `plexapi.audio`*

**READ Operations:**
- List artists
- List albums
- List tracks
- Get artist details
- Get album details
- Get track details
- View album art
- Get music genres

**WRITE Operations (with UNDO):**
- Update music metadata
- Rate tracks/albums
- Edit album art
- Delete music items

#### 3.4 **Photos**
*Module: `plexapi.photo`*

**READ Operations:**
- List photoalbums
- Browse photos
- Get photo metadata (EXIF, location, etc.)
- View thumbnails

**WRITE Operations (with UNDO):**
- Update photo metadata
- Delete photos/albums
- Organize photo albums

---

### 4. **Playback & Client Control**
*Module: `plexapi.client`, `plexapi.playqueue`*

**READ Operations:**
- List connected clients
- Get client details
- Get playback status
- Get current timeline
- List play queues
- Get play queue items

**WRITE Operations (with UNDO):**
- Play media on client
- Pause/Resume playback
- Stop playback
- Skip forward/backward
- Set volume
- Navigate client UI
- Create play queue
- Add to play queue
- Clear play queue

---

### 5. **Collections**
*Module: `plexapi.collection`*

**READ Operations:**
- List all collections
- Get collection details
- View collection items
- Get collection art

**WRITE Operations (with UNDO):**
- Create collection
- Add items to collection
- Remove items from collection
- Update collection metadata
- Delete collection
- Edit collection art

---

### 6. **Playlists**
*Module: `plexapi.playlist`*

**READ Operations:**
- List all playlists
- Get playlist details
- View playlist items
- Get playlist art

**WRITE Operations (with UNDO):**
- Create playlist
- Add items to playlist
- Remove items from playlist
- Reorder playlist items
- Update playlist metadata
- Delete playlist
- Copy playlist
- Edit playlist art

---

### 7. **User Management**
*Module: `plexapi.myplex`*

**READ Operations:**
- List users
- Get user details
- View shared libraries
- Get user permissions
- View user devices
- Get user watch history

**WRITE Operations (with UNDO):**
- Invite users
- Remove users
- Update user permissions
- Share/unshare libraries
- Update sharing settings

---

### 8. **MyPlex Account**
*Module: `plexapi.myplex`*

**READ Operations:**
- Get account details
- List owned servers
- List shared servers
- Get devices
- Get resources
- View subscriptions
- Get webhooks

**WRITE Operations (with UNDO):**
- Update account settings
- Create webhook
- Delete webhook
- Sign out devices

---

### 9. **Settings & Preferences**
*Module: `plexapi.settings`*

**READ Operations:**
- List all settings
- Get setting details
- View setting groups
- Get default values

**WRITE Operations (with UNDO):**
- Update settings
- Reset setting to default
- Batch update settings

---

### 10. **Discovery & Search**
*Module: `plexapi.server`, `plexapi.library`, `plexapi.gdm`*

**READ Operations:**
- Search across all libraries
- Advanced search with filters
- Search by hub (trending, popular, etc.)
- Discover servers (GDM)
- Get recommendations
- Get related items
- Get hub items

**WRITE Operations:**
- N/A (Read-only feature)

---

### 11. **Sync & Offline**
*Module: `plexapi.sync`*

**READ Operations:**
- List sync items
- Get sync status
- View sync settings
- Check sync space

**WRITE Operations (with UNDO):**
- Create sync item
- Update sync settings
- Cancel sync
- Delete sync item

---

### 12. **Alerts & Notifications**
*Module: `plexapi.alert`*

**READ Operations:**
- Listen for server alerts
- Get timeline updates
- Monitor status changes
- View activity feed

**WRITE Operations:**
- N/A (Monitoring feature)

---

### 13. **Sonos Integration**
*Module: `plexapi.sonos`*

**READ Operations:**
- Discover Sonos speakers
- Get Sonos playback status
- List available Sonos devices

**WRITE Operations (with UNDO):**
- Play media on Sonos
- Control Sonos playback
- Adjust Sonos volume

---

### 14. **Media Analysis**
*Module: `plexapi.media`*

**READ Operations:**
- Get media parts
- View video streams
- View audio streams
- View subtitle streams
- Get codec information
- View bitrate/resolution
- Get media metadata
- Check optimized versions

**WRITE Operations (with UNDO):**
- Analyze media
- Optimize media
- Delete optimized versions
- Select default streams

---

### 15. **Utilities & Tools**
*Module: `plexapi.utils`*

**READ Operations:**
- Download media
- Get download URLs
- Convert timestamps
- Parse XML responses
- Get thumbnails/art URLs

**WRITE Operations:**
- Upload media
- Upload artwork

---

## 🎨 Gallery UI Organization

The Gallery Mode will organize these features in a **hierarchical menu structure**:

```
GALLERY MODE
├── 📡 Server & Connection
│   ├── Connection Methods
│   ├── Server Information
│   ├── Sessions & Activity
│   └── Server Management
│
├── 📚 Library Management
│   ├── Library Sections
│   ├── Search & Discovery
│   ├── Statistics
│   └── Library Maintenance
│
├── 🎬 Media Operations
│   ├── Movies
│   ├── TV Shows
│   ├── Music
│   └── Photos
│
├── 🎮 Playback & Clients
│   ├── Client Discovery
│   ├── Playback Control
│   └── Play Queues
│
├── 📦 Collections & Playlists
│   ├── Collections
│   └── Playlists
│
├── 👥 Users & Sharing
│   ├── User Management
│   ├── Permissions
│   └── Sharing
│
├── 👤 MyPlex Account
│   ├── Account Details
│   ├── Servers
│   └── Devices
│
├── ⚙️ Settings & Preferences
│   ├── Server Settings
│   └── Preferences
│
├── 🔍 Search & Discovery
│   ├── Global Search
│   ├── Advanced Filters
│   └── Recommendations
│
├── 📱 Sync & Offline
│   ├── Sync Items
│   └── Sync Management
│
├── 🔔 Alerts & Monitoring
│   ├── Real-time Alerts
│   └── Activity Monitor
│
├── 🔊 Integrations
│   ├── Sonos
│   └── Other Devices
│
├── 🔬 Media Analysis
│   ├── Stream Information
│   ├── Codec Details
│   └── Optimization
│
└── 🛠️ Utilities
    ├── Downloads
    ├── Uploads
    └── Tools
```

---

## 🔄 UNDO System Design

For WRITE operations, PlexiGlass will implement a **snapshot-based undo system**:

1. **Pre-Write Snapshot**: Before any write operation, capture current state
2. **Execute Write**: Perform the requested operation
3. **Store Undo Data**: Save snapshot with restore instructions
4. **Undo Button**: Provide clear UI to undo the operation
5. **Restore**: If undo requested, restore from snapshot

Example undo operations:
- **Metadata change**: Store original metadata values
- **Collection modification**: Store original collection membership
- **Setting update**: Store original setting value
- **Deletion**: Store item reference (cannot fully undo, but warn user)
- **Playlist reorder**: Store original order

---

## 📊 Demo Data Requirements

Each demo will show:

1. **Purpose**: What this feature does and why you'd use it
2. **Code Example**: Actual python-plexapi code
3. **Live Result**: Real data from selected server
4. **Interactive Test**: Ability to modify parameters
5. **Write Test**: (if applicable) Test write with undo capability

---

**Status**: Planning Complete ✅  
**Next**: Begin implementation with TDD approach
