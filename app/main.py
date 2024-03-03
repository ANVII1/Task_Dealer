import logging as l
from utils.envvars import WEBHOOK_MODE
from modules.bot import dealer_bot

def setup_logging():
    """
    Setup logging settings
    """
    l.basicConfig(
    level=l.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs.log"
    )

def main() -> None:

    setup_logging()
    dealer_bot.run()

    l.info("Main ::: Start Working")
    
if __name__ == "__main__":
    main()