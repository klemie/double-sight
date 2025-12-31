import re
from typing import Optional

from models.constants import LAUNCH_EXT_VARS_REGEX
from ..models.models import BallData, Shot
from ...utils.Logging import Logger

def parse_shot_file(line: str) -> Optional[Shot]:
    """
    Parse a shot data file and extract relevant information to create a Shot object.
    """
    ball_data = None
    shot_number = None

    logger = Logger(__name__).get_logger()

    try:
        # only relevant part retained
        if 'LaunchExt Vars:' in line:
            logger.info("Found LaunchExt Vars")
            match = re.search(LAUNCH_EXT_VARS_REGEX, line)
            if match:
                sp, el, az, ts, sa, cy, shot_id = match.groups()
                ball_data = BallData(
                    Speed=float(sp),
                    SpinAxis=float(sa),
                    TotalSpin=float(ts),
                    HLA=float(az),
                    VLA=float(el)
                )
                shot_number = int(shot_id)

        if ball_data:
            shot = Shot()
            shot.BallData = ball_data
            if shot_number is not None:
                shot.ShotNumber = shot_number
            return shot

    except Exception as e:
        logger.error(f"Error parsing file: {e}")

    return None