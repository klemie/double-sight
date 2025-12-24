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

## WebSocket Protocol

### Connection

```
WS /ws
```

### Server-to-Client Messages

#### shot

Sent when a new shot is recorded.

```json
{
  "type": "shot",
  "ts": 1730000000.0,
  "shot": {
    "id": "uuid",
    "captured_at": "2025-12-23T19:01:02Z",
    "club": "7i",
    "metrics": {
      "carry": 165.2,
      "offline": -3.1,
      "ball_speed": 118.4,
      "spin": 6200
    },
    "session_id": "uuid",
    "is_outlier": false
  }
}
```

#### insight

Sent when a new insight is generated (typically follows a shot).

```json
{
  "type": "insight",
  "ts": 1730000001.2,
  "insight": {
    "id": "uuid",
    "club": "7i",
    "metric": "carry",
    "kind": "step_change",
    "window": "last_25",
    "baseline": "prev_25",
    "delta": 4.2,
    "ci": [1.1, 7.3],
    "p_value": 0.03,
    "effect_size": 0.52,
    "text": "7i carry is up +4.2y vs your previous 25 shots (95% CI +1.1 to +7.3)."
  }
}
```

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

