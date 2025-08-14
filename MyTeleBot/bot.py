import logging
import asyncio
import cohere
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from personality import SiegePersonality, HelpfulPersonality  # Import both personality classes
from config import Config

logger = logging.getLogger(__name__)

class SiegeBot:
    """
    A Telegram bot that can switch between a sarcastic and a helpful personality.
    """
    def __init__(self):
        self.config = Config()
        self.cohere_client = cohere.Client(self.config.cohere_api_key)
        self.application = None
        self.bot_username = "@Siege_Chat_Bot"
        self.personality_type = "siege"  # Default personality
        self.personality = SiegePersonality() # Instantiate the default personality
        
    async def start(self):
        """Initialize and start the bot"""
        try:
            token = self.config.telegram_token
            if not token:
                raise ValueError("Telegram token is required")
            self.application = Application.builder().token(token).build()
            
            # Add handlers
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("persona", self.set_persona)) # New persona command
            
            # Message handlers
            self.application.add_handler(MessageHandler(
                filters.TEXT & filters.REPLY, 
                self.handle_reply
            ))
            self.application.add_handler(MessageHandler(
                filters.TEXT & filters.Entity("mention"), 
                self.handle_mention
            ))
            self.application.add_handler(MessageHandler(
                filters.TEXT & filters.ChatType.PRIVATE, 
                self.handle_private_message
            ))
            
            logger.info("Starting bot...")
            await self.application.initialize()
            await self.application.start()
            if self.application.updater:
                await self.application.updater.start_polling()
            
            logger.info("Bot is running! Press Ctrl+C to stop.")
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            if self.application:
                await self.application.stop()
                
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        if not update.message:
            return
        response = self.personality.get_start_message()
        await update.message.reply_text(response)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        if not update.message:
            return
        response = self.personality.get_help_message()
        await update.message.reply_text(response)

    async def set_persona(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /persona command to switch personalities."""
        if not update.message or not context.args:
            await update.message.reply_text("Please specify a persona. Example: /persona helpful or /persona siege")
            return
        
        new_persona = context.args[0].lower()
        if new_persona == "helpful":
            self.personality = HelpfulPersonality()
            self.personality_type = "helpful"
            await update.message.reply_text("Persona switched to helpful. I will now respond in a friendly and informative manner. 😊")
        elif new_persona == "siege":
            self.personality = SiegePersonality()
            self.personality_type = "siege"
            await update.message.reply_text("Persona switched back to siege. Prepare for sass and bluntness.")
        else:
            await update.message.reply_text("Invalid persona. Please choose 'helpful' or 'siege'.")

    # The rest of the handler functions remain the same as the original bot.py
    # ... (handle_private_message, handle_mention, handle_reply) ...

    async def handle_private_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text: return
        user_message = update.message.text
        user_name = update.effective_user.username or update.effective_user.first_name or "stranger" if update.effective_user else "stranger"
        try:
            response = await self.generate_response(user_message, user_name, is_private=True)
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error handling private message: {e}")
            fallback_response = self.personality.get_error_response()
            await update.message.reply_text(fallback_response)
            
    async def handle_mention(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text: return
        user_message = update.message.text
        user_name = update.effective_user.username or update.effective_user.first_name or "stranger" if update.effective_user else "stranger"
        if self.bot_username.lower() in user_message.lower():
            try:
                response = await self.generate_response(user_message, user_name, is_mention=True)
                await update.message.reply_text(response)
            except Exception as e:
                logger.error(f"Error handling mention: {e}")
                fallback_response = self.personality.get_error_response()
                await update.message.reply_text(fallback_response)
                
    async def handle_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message or not update.message.text: return
        if (update.message.reply_to_message and update.message.reply_to_message.from_user and update.message.reply_to_message.from_user.is_bot):
            user_message = update.message.text
            user_name = update.effective_user.username or update.effective_user.first_name or "stranger" if update.effective_user else "stranger"
            try:
                response = await self.generate_response(user_message, user_name, is_reply=True)
                await update.message.reply_text(response)
            except Exception as e:
                logger.error(f"Error handling reply: {e}")
                fallback_response = self.personality.get_error_response()
                await update.message.reply_text(fallback_response)

    def is_special_query(self, message: str) -> str | None:
        """
        Check if the message is a special query for date/time or business info.
        This function is only used when the 'helpful' personality is active.
        """
        message_lower = message.lower()
        if ("date" in message_lower and "time" in message_lower) or "what time is it" in message_lower:
            return "datetime"
        if "phone number" in message_lower or "address" in message_lower:
            return "business"
        question_indicators = ['what is', 'who is', 'when did', 'where is', 'how did', 'why did', 'tell me about', 'explain']
        if any(indicator in message_lower for indicator in question_indicators):
            return "wiki"
        return None

    async def generate_response(self, user_message: str, user_name: str, is_private=False, is_mention=False, is_reply=False):
        """Generate AI response using Cohere API, with logic for different personalities."""
        try:
            if self.personality_type == "helpful":
                query_type = self.is_special_query(user_message)
                
                if query_type == "datetime":
                    response_text = self.personality.get_current_datetime()
                elif query_type == "business":
                    response_text = self.personality.search_business_info(user_message)
                elif query_type == "wiki":
                    response_text = self.personality.search_wikipedia(user_message)
                else:
                    prompt = self.personality.create_prompt(user_message, user_name, is_private, is_mention, is_reply)
                    cohere_response = self.cohere_client.generate(
                        model='command',
                        prompt=prompt,
                        max_tokens=200,
                        temperature=0.7,
                        stop_sequences=["\n\n", "Human:", "User:"]
                    )
                    generated_text = cohere_response.generations[0].text.strip()
                    response_text = self.personality.post_process_response(generated_text)
            else: # siege personality
                prompt = self.personality.create_prompt(user_message, user_name, is_private, is_mention, is_reply)
                wiki_info = ""
                if self.personality.is_science_history_question(user_message):
                    wiki_result = self.personality.search_wikipedia(user_message)
                    if wiki_result and "Wikipedia failed" not in wiki_result and "Couldn't find" not in wiki_result:
                        wiki_info = f"\n\nWikipedia info: {wiki_result}"
                
                prompt = self.personality.create_prompt(
                    user_message + wiki_info, 
                    user_name, 
                    is_private=is_private, 
                    is_mention=is_mention, 
                    is_reply=is_reply
                )
                cohere_response = self.cohere_client.generate(
                    model='command',
                    prompt=prompt,
                    max_tokens=100,
                    temperature=0.8,
                    stop_sequences=["\n\n", "Human:", "User:"]
                )
                generated_text = cohere_response.generations[0].text.strip()
                response_text = self.personality.post_process_response(generated_text)

            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self.personality.get_fallback_response()
