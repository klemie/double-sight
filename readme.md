# Longitudinal Shot Trend Analysis

## Objective

Continuously analyze shot data over time and generate statistically grounded trend commentary (per club and overall), delivered via API/WebSocket to a React UI.

## Core Outputs

1. **Club Trends:** carry, offline, ball speed, spin, launch (level + direction of change).
2. **Consistency:** dispersion/variance changes over time.
3. **Insight Feed:** short comments with magnitude + confidence, e.g. “7i carry up +4.2y vs last 30d (95% CI +1.1 to +7.3).”

## Insight Types (MVP)

-**Trend (slope):** metric trending up/down over last N shots / last X days.

-   **Step change:** recent window vs prior window difference (e.g., last 25 vs previous 25).
-   Consistency change: SD/IQR or dispersion area up/down vs baseline.
-   **Bias shift:** mean offline/azimuth shift (left/right) vs baseline.
-   **Data quality:** insufficient data / outlier-heavy warnings.

## Statistics (MVP Toolkit)

-   Windows: `last_10`, `last_25`, `last_50`, `last_7d`, `last_30d` (configurable).
-   Baseline: rolling `30d` (plus optional lifetime).
-   Robust summaries: median + IQR; mean + SD (both stored).
-   Trend: simple linear regression on time (or shot index) + CI for slope.
-   Step change: difference in means (and medians) + CI + effect size (Cohen’s d).
-   Outliers: MAD-based tagging; exclude from trend/step if enabled (but keep visible).

### Guardrails

-   Minimum sample to claim: default n >= 20 for trend, n >= 10 per window for step change.
-   If insufficient data: no claim, only “insufficient data”.

## Requirements

**Ubiquitous**

R-STAT-1: The system shall compute rolling statistics per club for configured windows.

R-STAT-2: The system shall compute baseline statistics per club (default 30 days).

R-STAT-3: The system shall generate insight statements containing: metric, direction, magnitude, window/baseline, and confidence.

**Event-driven**

R-STAT-4: When a new shot is persisted, the system shall update rollups for the shot’s club.

R-STAT-5: When an insight passes configured significance/thresholds, the system shall emit an insight event to connected clients.

**State-driven**

R-STAT-6: While a session is active, the system shall compute session-only statistics and present them separately from baseline trends.

**Optional**

R-STAT-7: Where shots are tagged (e.g., “lesson”, “new shaft”), the system may compute before/after comparisons by tag segment.

R-STAT-8: The system may exclude tagged outliers from trend estimation while preserving them in storage and UI.

**Unwanted**

R-STAT-9: If data is insufficient for a metric/window, the system shall not generate a trend claim for that metric/window.

Data/Storage Additions

shots: canonical metrics + raw_json, signature, captured_at, club, session_id, is_outlier (bool), outlier_reason.

rollups_club_window: precomputed stats by (club, window) (mean, sd, median, iqr, n, updated_at).

insights: (id, club, metric, type, window, baseline, value_delta, slope, ci_low, ci_high, p_value, effect_size, created_at, text).

Event Schema
WebSocket: shot

```json
{
    "type": "shot",
    "ts": 1730000000.0,
    "shot": {
        "id": "…",
        "captured_at": "2025-12-23T19:01:02Z",
        "club": "7i",
        "metrics": {
            "carry": 165.2,
            "offline": -3.1,
            "ball_speed": 118.4,
            "spin": 6200
        },
        "session_id": "…",
        "is_outlier": false
    }
}
```

WebSocket: insight

```json
{
    "type": "insight",
    "ts": 1730000001.2,
    "insight": {
        "id": "…",
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
