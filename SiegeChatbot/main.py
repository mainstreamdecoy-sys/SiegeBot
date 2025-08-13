import asyncio
import signal
import sys
import logging
from telegram_integration import SiegeTelegramBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global bot instance
bot_instance = None

async def main():
    """Main function to run the Siege Telegram bot"""
    global bot_instance
    
    try:
        # Create and start Siege
        bot_instance = SiegeTelegramBot()
        logger.info("Siege Chat Bot initialized successfully")
        
        # Start the bot
        await bot_instance.run()
        
    except KeyboardInterrupt:
        logger.info("Siege terminated by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down Siege...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run Siege
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Siege stopped")
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)
