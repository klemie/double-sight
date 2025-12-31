import os
import time

from parser.parse import parse_shot_file
from ..models.models import BallData, Shot, ShotDataOptions
from ..models.constants import OUTPUT_LOG_PATH
from ...utils.Logging import Logger

# The hidden path where Unity stores GSPro logs
LOG_PATH = os.path.expandvars(OUTPUT_LOG_PATH)

logger = Logger(__name__).get_logger()

def sniff_gspro():
    logger.info(f"Sniffer Active on: {LOG_PATH}")
    
    # We use 'rb' (read binary) and a manual decode to avoid encoding locks
    with open(LOG_PATH, 'rb') as f:
        # Move to the end of the file so we don't process history
        f.seek(0, os.SEEK_END)
        
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)  # Wait for GSPro to write more
                continue
            
            # Convert binary to string
            decoded_line = line.decode('utf-8', errors='ignore').strip()
            data = parse_shot_file(decoded_line)

            if data:
                logger.info(f"Parsed data: {data}")


if __name__ == "__main__":
    if os.path.exists(LOG_PATH):
        sniff_gspro()
    else:
        logger.error("Log file not found. Launch GSPro first!")