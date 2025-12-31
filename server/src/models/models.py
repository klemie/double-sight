from dataclasses import dataclass, field, fields
from models.constants import BASE_UNITS, DEVICE_ID
from typing import Any, Any, Optional

# -------------
# Socket Models
# ------------- 

@dataclass
class BallData:
    Speed: float
    SpinAxis: float
    TotalSpin: float
    HLA: float
    VLA: float

@dataclass
class ShotDataOptions:
    ContainsBallData: bool = True
    ContainsClubData: bool = False
    LaunchMonitorIsReady: bool | None = None
    LaunchMonitorBallDetected: bool | None = None
    IsHeartbeat: bool | None = None

@dataclass
class Shot:
    DeviceID: str = DEVICE_ID
    Units: str = BASE_UNITS
    ShotNumber: int = -1
    APIVersion: str = "1"
    BallData: BallData = None
    ShotDataOptions: ShotDataOptions = field(default_factory=ShotDataOptions)

@dataclass
class GSProPlayer:
    Handed: str | None = None
    Club: str | None = None
    DistanceToTarget: float | None = None

@dataclass
class GSProMessage:
    Code: int
    Message: str | None = None
    Player: GSProPlayer | None = None
    Xtra: dict = field(default_factory=dict)  # other attributes passed through in extra

    @classmethod
    def create_from_dict(cls, dct: dict[str, Any]) -> GSProMessage:
        dct = dict(dct)
        kwargs = {}
        for f in fields(cls):
            if f.name in dct:
                kwargs[f.name] = dct.pop(f.name)
        kwargs["Xtra"] = dct
        return cls(**kwargs)
