import logging
import os


# ==================================================
# Create Logs Directory
# ==================================================

LOG_DIR = "logs"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


# ==================================================
# Configure Logger
# ==================================================

LOG_FILE = os.path.join(
    LOG_DIR,
    "agent.log"
)


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)


# ==================================================
# Logging Helper
# ==================================================

def log_event(
    node: str,
    message: str
):

    logging.info(
        f"{node} | {message}"
    )

