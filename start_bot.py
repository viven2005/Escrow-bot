#!/usr/bin/env python3
"""
QuickEscrowBot Launcher
Production-ready Telegram bot with proper error handling
"""

import os
import sys
import time
import logging
import requests
from pathlib import Path

# Add bot directory to path
sys.path.append(str(Path(__file__).parent / "bot"))

from telegram_bot import QuickEscrowBot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

def check_api_connection():
    """Check if the API server is accessible"""
    api_url = "http://0.0.0.0:5000/api/stats"
    try:
        response = requests.get(api_url, timeout=5)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"API connection failed: {e}")
        return False

def main():
    """Main function to run the bot"""
    logger.info("🛡️ Starting QuickEscrowBot...")
    
    # Check environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN environment variable is required")
        return
    
    # Check API connection
    logger.info("🔍 Checking API connection...")
    if not check_api_connection():
        logger.warning("⚠️ API server not accessible, bot will continue but may have limited functionality")
    else:
        logger.info("✅ API connection established")
    
    try:
        # Initialize bot
        bot = QuickEscrowBot()
        logger.info("✅ Bot initialized successfully!")
        
        # Start the bot
        logger.info("🚀 Bot is now running and ready to receive messages...")
        logger.info("💡 Send /start to the bot to begin interaction")
        
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Error running bot: {e}")
        return 1

if __name__ == "__main__":
    exit(main() or 0)