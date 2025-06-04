import logging

from app.app import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("main")

if __name__ == "__main__":
    logger.info("Running app in debug mode")
    app.run(debug=True, dev_tools_ui=True)
