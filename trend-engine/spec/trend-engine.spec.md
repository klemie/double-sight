# Trend Engine Specification

## Overview

Statistical analysis library for computing rolling statistics, detecting trends, and generating human-readable insights from golf shot data. Can be used as an importable library or run as a standalone service.

## Technology Stack

- Python 3.11+
- NumPy for numerical computation
- SciPy for statistical functions
- Pydantic for data validation
- Pyright for static type checking
- Ruff for linting and formatting
- pytest for testing

## Usage Modes

### As Library

```python
from trend_engine import compute_rollups, generate_insights
from trend_engine.models import Shot, Rollup, Insight

# Process a new shot
rollups = compute_rollups(club="7i", shots=shots)
insights = generate_insights(club="7i", rollups=rollups, config=config)
```

### As Service

```bash
trend-engine serve --port 8001
```

Provides REST API for batch processing and WebSocket for streaming analysis.

## Pydantic Models

### Shot

```python
class ShotMetrics(BaseModel):
    carry: float           # Carry distance in yards
    offline: float         # Offline distance (negative = left)
    ball_speed: float      # Ball speed in mph
    spin: int              # Spin rate in rpm
    launch_angle: float | None = None
    launch_direction: float | None = None

class Shot(BaseModel):
    id: str
    captured_at: datetime
    club: str
    metrics: ShotMetrics
    session_id: str | None = None
    is_outlier: bool = False
    outlier_reason: str | None = None
```

### Rollup

```python
class Rollup(BaseModel):
    club: str
    window: str            # "last_10", "last_25", "last_50", "last_7d", "last_30d"
    metric: str            # "carry", "offline", "ball_speed", "spin"
    mean: float
    sd: float              # Standard deviation
    median: float
    iqr: float             # Interquartile range
    n: int                 # Sample size
    updated_at: datetime
```

### Insight

```python
class Insight(BaseModel):
    id: str
    club: str
    metric: str
    kind: Literal["trend", "step_change", "consistency", "bias_shift"]
    window: str
    baseline: str
    delta: float
    slope: float | None = None
    ci: tuple[float, float]
    p_value: float
    effect_size: float
    text: str
    created_at: datetime
```

## Statistical Methods

### Rolling Statistics (compute_rollups)

For each configured window, compute:

- **Mean** - arithmetic average
- **Standard Deviation** - population SD
- **Median** - 50th percentile (robust to outliers)
- **IQR** - interquartile range (Q3 - Q1)
- **Sample Size** - number of shots in window

### Windows

| Window | Definition |
|--------|------------|
| last_10 | Most recent 10 shots |
| last_25 | Most recent 25 shots |
| last_50 | Most recent 50 shots |
| last_7d | Shots from past 7 days |
| last_30d | Shots from past 30 days |

### Trend Detection (Linear Regression)

Fit OLS regression: `metric ~ time` or `metric ~ shot_index`

```python
def compute_trend(shots: list[Shot], metric: str) -> TrendResult:
    """
    Returns:
        slope: change per unit time
        ci: 95% confidence interval for slope
        p_value: significance of slope != 0
        r_squared: explained variance
    """
```

Minimum sample: n >= 20

### Step Change Detection

Compare two adjacent windows (e.g., last_25 vs prev_25):

```python
def compute_step_change(
    current: list[Shot],
    previous: list[Shot],
    metric: str
) -> StepChangeResult:
    """
    Returns:
        delta: difference in means
        ci: 95% confidence interval for difference
        p_value: t-test p-value
        effect_size: Cohen's d
    """
```

Minimum sample: n >= 10 per window

### Consistency Change

Compare variance/dispersion between windows:

- SD ratio test
- IQR comparison
- Levene's test for equality of variances

### Bias Shift

Detect systematic left/right shift in offline metric:

- Compare mean offline between windows
- One-sample t-test against 0 (unbiased baseline)

### Outlier Detection

Use MAD (Median Absolute Deviation) method:

```python
def detect_outliers(values: list[float], threshold: float = 3.0) -> list[bool]:
    """
    Mark values where |x - median| / MAD > threshold as outliers.
    """
```

## Insight Generation

### Thresholds

| Insight Type | Minimum n | p-value | Effect Size |
|--------------|-----------|---------|-------------|
| trend | 20 | < 0.05 | |slope| > 0.1 |
| step_change | 10/window | < 0.05 | |d| > 0.3 |
| consistency | 10/window | < 0.10 | ratio > 1.5 |
| bias_shift | 20 | < 0.05 | |shift| > 2y |

### Text Generation

Format insights with:
- Metric name and club
- Direction (up/down/left/right)
- Magnitude with units
- Confidence interval
- Window context

Example outputs:
- "7i carry is up +4.2y vs your previous 25 shots (95% CI +1.1 to +7.3)."
- "Driver offline has shifted 3.1y left over last 30 days (p=0.02)."
- "5i consistency improved: dispersion down 15% vs last month."

## Configuration

```python
class TrendEngineConfig(BaseModel):
    windows: list[str] = ["last_10", "last_25", "last_50", "last_7d", "last_30d"]
    baseline_window: str = "last_30d"
    min_samples_trend: int = 20
    min_samples_step: int = 10
    p_value_threshold: float = 0.05
    effect_size_threshold: float = 0.3
    exclude_outliers: bool = True
    outlier_mad_threshold: float = 3.0
```

## API Contract (Service Mode)

### POST /analyze

Batch analysis of shots.

```json
{
  "club": "7i",
  "shots": [...],
  "config": {}
}
```

Response:

```json
{
  "rollups": [...],
  "insights": [...]
}
```

### WebSocket /ws

Stream shots and receive insights in real-time.

## Requirements Mapping

| Requirement | Implementation |
|-------------|----------------|
| R-STAT-1 | compute_rollups() for all configured windows |
| R-STAT-2 | baseline_window defaults to 30d |
| R-STAT-3 | Insight model includes all required fields |
| R-STAT-7 | Tag-based segmentation in generate_insights() |
| R-STAT-8 | exclude_outliers config option |
| R-STAT-9 | Return None/empty when n < min_samples |

## Testing Strategy

- Unit tests for each statistical function
- Property-based tests for edge cases (empty data, single point)
- Integration tests for full analysis pipeline
- Benchmark tests for performance on large datasets
- Coverage threshold: 80%

