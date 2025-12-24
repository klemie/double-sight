# Client Specification

## Overview

React-based dashboard for displaying real-time shot data and trend insights from the Double Sight system. Uses MobX for state management and WebSocket for live updates.

## Technology Stack

- React 18 with TypeScript (strict mode)
- MobX for reactive state management
- Vite for bundling and dev server
- Vitest for unit testing

## WebSocket Connection

### Connection Lifecycle

1. Connect to `/ws` endpoint on mount
2. Authenticate with session token (future)
3. Listen for `shot` and `insight` events
4. Auto-reconnect with exponential backoff on disconnect

### Message Handlers

```typescript
interface WebSocketMessage {
  type: "shot" | "insight";
  ts: number;
  shot?: Shot;
  insight?: Insight;
}
```

## MobX Store Structure

### RootStore

Central store that composes all domain stores.

### ShotStore

- `shots: Shot[]` - All shots in current view
- `shotsByClub: Map<string, Shot[]>` - Shots grouped by club
- `addShot(shot: Shot): void` - Add incoming shot from WebSocket
- `loadShots(params: LoadParams): Promise<void>` - Fetch historical shots

### InsightStore

- `insights: Insight[]` - All insights
- `insightsByClub: Map<string, Insight[]>` - Insights grouped by club
- `activeInsights: Insight[]` - Recent/highlighted insights
- `addInsight(insight: Insight): void` - Add incoming insight from WebSocket

### SessionStore

- `currentSession: Session | null` - Active practice session
- `isSessionActive: boolean` - Whether a session is in progress
- `sessionStats: SessionStats` - Computed session statistics

### UIStore

- `selectedClub: string | null` - Currently selected club filter
- `selectedMetric: Metric` - Active metric for trend display
- `timeWindow: TimeWindow` - Selected time window

## Component Hierarchy

```
App
├── Header
│   └── SessionIndicator
├── ClubSelector
├── MainPanel
│   ├── ShotFeed
│   │   └── ShotCard
│   ├── TrendChart
│   └── StatsPanel
│       ├── MetricCard
│       └── ComparisonWidget
└── InsightFeed
    └── InsightCard
```

## Data Types

### Shot

```typescript
interface Shot {
  id: string;
  captured_at: string;
  club: string;
  metrics: {
    carry: number;
    offline: number;
    ball_speed: number;
    spin: number;
    launch_angle?: number;
    launch_direction?: number;
  };
  session_id: string | null;
  is_outlier: boolean;
}
```

### Insight

```typescript
interface Insight {
  id: string;
  club: string;
  metric: string;
  kind: "trend" | "step_change" | "consistency" | "bias_shift";
  window: string;
  baseline: string;
  delta: number;
  ci: [number, number];
  p_value: number;
  effect_size: number;
  text: string;
}
```

## Real-Time Update Flow

1. WebSocket receives `shot` event
2. `ShotStore.addShot()` appends shot to state
3. MobX observers trigger re-render of `ShotFeed` and `TrendChart`
4. WebSocket receives `insight` event (may follow shot)
5. `InsightStore.addInsight()` appends insight
6. `InsightFeed` displays new insight with animation

## Requirements Mapping

| Requirement | Implementation |
|-------------|----------------|
| R-STAT-5 | InsightStore receives insight events via WebSocket |
| R-STAT-6 | SessionStore.sessionStats computed from session-only shots |

## Testing Strategy

- Unit tests for MobX store actions and computed values
- Component tests with @testing-library/react
- WebSocket mock for integration tests
- Coverage threshold: 80%

