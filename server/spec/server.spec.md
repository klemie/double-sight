# Server Specification

## Overview

FastAPI-based backend server providing REST API and WebSocket endpoints for shot tracking, trend analysis, and real-time insight delivery.

## Technology Stack

- Python 3.11+
- FastAPI for web framework
- Pydantic for data validation
- SQLAlchemy + aiosqlite for database
- Pyright for static type checking
- Ruff for linting and formatting
- pytest for testing

## API Endpoints

### Shots

```
GET    /api/shots              List shots with pagination and filters
GET    /api/shots/{id}         Get single shot by ID
POST   /api/shots              Create new shot (from launch monitor)
DELETE /api/shots/{id}         Delete shot (soft delete)
```

### Clubs

```
GET    /api/clubs              List all clubs with shot counts
GET    /api/clubs/{club}/stats Get current stats for a club
```

### Sessions

```
GET    /api/sessions           List practice sessions
GET    /api/sessions/{id}      Get session details with shots
POST   /api/sessions           Start new session
PATCH  /api/sessions/{id}      End session / update notes
```

### Insights

```
GET    /api/insights           List insights with filters
GET    /api/insights/{id}      Get single insight
```

## Socket Protocol

Connecting to GSPro. Cant use socket, so must read from a freakin file :)

### Connection



### Connection Management

- Heartbeat ping/pong every 30 seconds
- Auto-reconnect recommended on client side
- Connection state tracked per client

## Database Schema

### shots

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| captured_at | TIMESTAMP | When shot was taken |
| club | VARCHAR | Club identifier (e.g., "7i", "DR") |
| carry | FLOAT | Carry distance (yards) |
| offline | FLOAT | Offline distance (yards, negative=left) |
| ball_speed | FLOAT | Ball speed (mph) |
| spin | INT | Spin rate (rpm) |
| launch_angle | FLOAT | Launch angle (degrees) |
| launch_direction | FLOAT | Launch direction (degrees) |
| session_id | UUID | Foreign key to sessions |
| is_outlier | BOOLEAN | Flagged as outlier |
| outlier_reason | VARCHAR | Reason for outlier flag |
| raw_json | JSON | Original launch monitor data |
| signature | VARCHAR | Hash for deduplication |
| created_at | TIMESTAMP | Record creation time |

### rollups_club_window

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| club | VARCHAR | Club identifier |
| window | VARCHAR | Window type (last_10, last_25, etc.) |
| metric | VARCHAR | Metric name |
| mean | FLOAT | Mean value |
| sd | FLOAT | Standard deviation |
| median | FLOAT | Median value |
| iqr | FLOAT | Interquartile range |
| n | INT | Sample size |
| updated_at | TIMESTAMP | Last update time |

### insights

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| club | VARCHAR | Club identifier |
| metric | VARCHAR | Metric name |
| kind | VARCHAR | Insight type (trend, step_change, etc.) |
| window | VARCHAR | Analysis window |
| baseline | VARCHAR | Comparison baseline |
| delta | FLOAT | Change magnitude |
| slope | FLOAT | Trend slope (if applicable) |
| ci_low | FLOAT | Confidence interval lower bound |
| ci_high | FLOAT | Confidence interval upper bound |
| p_value | FLOAT | Statistical significance |
| effect_size | FLOAT | Cohen's d or similar |
| text | TEXT | Human-readable insight |
| created_at | TIMESTAMP | When insight was generated |

### sessions

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| started_at | TIMESTAMP | Session start time |
| ended_at | TIMESTAMP | Session end time (null if active) |
| notes | TEXT | User notes |

## Integration with Trend Engine

The server imports `trend_engine` as a library:

```python
from trend_engine import compute_rollups, generate_insights
from trend_engine.models import Shot, Insight
```

### Shot Processing Flow

1. Receive shot via POST /api/shots or external integration
2. Validate and persist shot
3. Call `trend_engine.compute_rollups(club, shot)` to update statistics
4. Call `trend_engine.generate_insights(club)` to check for new insights
5. Broadcast shot and any insights via WebSocket

## Requirements Mapping

| Requirement | Implementation |
|-------------|----------------|
| R-STAT-1 | trend_engine.compute_rollups() called on each shot |
| R-STAT-4 | Shot handler triggers rollup update |
| R-STAT-5 | WebSocket broadcasts insights when generated |
| R-STAT-9 | trend_engine returns None for insufficient data |

## Testing Strategy

- Unit tests for API endpoints using TestClient
- Integration tests with in-memory SQLite
- WebSocket tests with async test client
- Coverage threshold: 80%

