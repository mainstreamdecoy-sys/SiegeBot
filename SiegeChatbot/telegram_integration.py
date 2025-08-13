#!/usr/bin/env python3
"""
Direct Telegram Bot API integration for Siege
Bypasses python-telegram-bot library import issues
"""

import asyncio
import aiohttp
import json
import logging
from typing import Dict, Optional
from siege_bot import SiegeChatBot
from config import Config

logger = logging.getLogger(__name__)

class TelegramAPI:
    """Direct Telegram Bot API client"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_updates(self, offset: int = 0, timeout: int = 30) -> Dict:
        """Get updates from Telegram"""
        url = f"{self.base_url}/getUpdates"
        params = {
            "offset": offset,
            "timeout": timeout,
            "allowed_updates": json.dumps(["message"])
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Failed to get updates: {e}")
            return {"ok": False, "result": []}
    
    async def send_message(self, chat_id: int, text: str, reply_to_message_id: Optional[int] = None) -> Dict:
        """Send message to Telegram chat"""
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
        
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
            
        try:
            async with self.session.post(url, json=data) as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {"ok": False}
    
    async def send_chat_action(self, chat_id: int, action: str = "typing"):
        """Send chat action (typing indicator)"""
        url = f"{self.base_url}/sendChatAction"
        data = {
            "chat_id": chat_id,
            "action": action
        }
        
        try:
            async with self.session.post(url, json=data) as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Failed to send chat action: {e}")

class SiegeTelegramBot:
    """Siege bot with direct Telegram integration"""
    
    def __init__(self):
        self.siege = SiegeChatBot()
        self.api = TelegramAPI(Config.TELEGRAM_BOT_TOKEN)
        self.last_update_id = 0
        self.bot_username = Config.BOT_USERNAME
        
    def _should_respond_to_message(self, message: Dict) -> bool:
        """Check if Siege should respond to this message"""
        text = message.get("text", "")
        
        # Check for mention
        if f"@{self.bot_username}" in text:
            return True
            
        # Check if replying to bot message
        reply_to = message.get("reply_to_message")
        if reply_to and reply_to.get("from", {}).get("is_bot"):
            return True
            
        return False
    
    def _extract_message_content(self, text: str) -> str:
        """Extract clean message content"""
        # Remove bot mention
        clean_text = text.replace(f"@{self.bot_username}", "").strip()
        return clean_text
    
    async def handle_message(self, message: Dict):
        """Process incoming message"""
        try:
            chat_id = message["chat"]["id"]
            message_id = message["message_id"]
            text = message.get("text", "")
            user = message.get("from", {})
            user_name = user.get("first_name", "User")
            
            logger.info(f"Processing message from {user_name}: {text[:50]}...")
            
            # Handle commands
            if text.startswith("/start"):
                response = self.siege.start_command_response()
                await self.api.send_message(chat_id, response, message_id)
                return
                
            elif text.startswith("/help"):
                response = self.siege.help_command_response()
                await self.api.send_message(chat_id, response, message_id)
                return
            
            # Check if should respond to regular message
            if not self._should_respond_to_message(message):
                return
                
            # Extract clean message content
            clean_message = self._extract_message_content(text)
            if not clean_message.strip():
                await self.api.send_message(
                    chat_id, 
                    "Did you just mention me with nothing to say? How absolutely cringe.",
                    message_id
                )
                return
            
            # Show typing indicator
            await self.api.send_chat_action(chat_id, "typing")
            
            # Generate Siege's response
            response = await self.siege.generate_response(clean_message, user_name)
            
            # Send response
            await self.api.send_message(chat_id, response, message_id)
            logger.info(f"Sent response to {user_name}")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            try:
                await self.api.send_message(
                    chat_id,
                    "My android brain just blue-screened. Even future tech has its limits.",
                    message_id
                )
            except:
                pass
    
    async def process_updates(self, updates: Dict):
        """Process all updates from Telegram"""
        if not updates.get("ok", False):
            return
            
        for update in updates.get("result", []):
            self.last_update_id = max(self.last_update_id, update["update_id"])
            
            if "message" in update:
                await self.handle_message(update["message"])
    
    async def run(self):
        """Main bot loop"""
        logger.info("Starting Siege Chat Bot...")
        
        async with self.api:
            logger.info("Connected to Telegram API")
            
            while True:
                try:
                    # Get updates
                    updates = await self.api.get_updates(
                        offset=self.last_update_id + 1,
                        timeout=30
                    )
                    
                    # Process updates
                    await self.process_updates(updates)
                    
                except KeyboardInterrupt:
                    logger.info("Bot stopped by user")
                    break
                except Exception as e:
                    logger.error(f"Error in main loop: {e}")
                    await asyncio.sleep(5)  # Wait before retrying

async def main():
    """Run the Siege bot"""
    try:
        bot = SiegeTelegramBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")

if __name__ == "__main__":
    asyncio.run(main())