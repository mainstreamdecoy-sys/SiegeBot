import logging
import asyncio
import cohere
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from telegram.error import TelegramError, NetworkError, RetryAfter
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

class SiegeChatBot:
    """Telegram chatbot powered by Cohere AI"""
    
    def __init__(self):
        """Initialize the bot with configuration and API clients"""
        Config.validate()
        
        # Initialize Cohere client
        try:
            self.cohere_client = cohere.Client(api_key=Config.COHERE_API_KEY)
            logger.info("Cohere client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {e}")
            raise
        
        # Initialize Telegram application
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Set up handlers
        self._setup_handlers()
        
        # Store bot info
        self.bot_username = f"@{Config.BOT_USERNAME}"
        
    def _setup_handlers(self):
        """Set up message handlers for the bot"""
        
        # Handle start command
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Handle mentions and replies
        mention_filter = filters.TEXT & (
            filters.Mention(Config.BOT_USERNAME) | 
            filters.REPLY
        )
        
        self.application.add_handler(
            MessageHandler(mention_filter, self.handle_message)
        )
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
        
        logger.info("Message handlers set up successfully")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            f"👋 Hello! I'm {Config.BOT_USERNAME}, an AI-powered chatbot.\n\n"
            "I can help answer questions and have conversations with you!\n\n"
            "💬 **How to interact with me:**\n"
            f"• Mention me with {self.bot_username} followed by your message\n"
            "• Reply to any of my messages\n\n"
            "🚀 Try asking me anything!"
        )
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        logger.info(f"Start command used by user {update.effective_user.id}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = (
            f"🤖 **{Config.BOT_USERNAME} Help**\n\n"
            "**Commands:**\n"
            "• `/start` - Welcome message\n"
            "• `/help` - Show this help message\n\n"
            "**How to chat with me:**\n"
            f"• Mention me: `{self.bot_username} your question here`\n"
            "• Reply to my messages directly\n\n"
            "**Examples:**\n"
            f"• `{self.bot_username} What's the weather like today?`\n"
            f"• `{self.bot_username} Tell me a joke`\n"
            f"• `{self.bot_username} Explain quantum physics`\n\n"
            "💡 I'm powered by Cohere AI and can help with various topics!"
        )
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
        logger.info(f"Help command used by user {update.effective_user.id}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle messages that mention the bot or reply to bot messages"""
        
        if not update.message or not update.message.text:
            return
        
        message = update.message
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "User"
        
        logger.info(f"Processing message from user {user_id} ({user_name})")
        
        # Check if this is a mention or reply to bot
        is_mention = self.bot_username.lower() in message.text.lower()
        is_reply_to_bot = (
            message.reply_to_message and 
            message.reply_to_message.from_user.id == context.bot.id
        )
        
        if not (is_mention or is_reply_to_bot):
            return
        
        # Extract the actual message content
        user_message = self._extract_message_content(message.text, is_mention)
        
        if not user_message.strip():
            await message.reply_text(
                "🤔 I noticed you mentioned me, but I couldn't find a question or message to respond to. "
                "Try asking me something!"
            )
            return
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Generate response using Cohere
            ai_response = await self._generate_cohere_response(user_message, user_name)
            
            # Send response
            await message.reply_text(ai_response)
            
            logger.info(f"Successfully responded to user {user_id}")
            
        except Exception as e:
            logger.error(f"Error processing message from user {user_id}: {e}")
            error_message = (
                "🚫 Sorry, I encountered an error while processing your message. "
                "Please try again in a moment."
            )
            await message.reply_text(error_message)
    
    def _extract_message_content(self, text: str, is_mention: bool) -> str:
        """Extract the actual message content from the text"""
        if is_mention:
            # Remove the bot mention from the message
            import re
            # Remove @bot_username from the message
            pattern = r'@' + Config.BOT_USERNAME + r'\b'
            cleaned_text = re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
            return cleaned_text
        else:
            # For replies, use the full message
            return text.strip()
    
    async def _generate_cohere_response(self, user_message: str, user_name: str) -> str:
        """Generate a response using Cohere API"""
        
        try:
            # Create a conversational prompt
            prompt = (
                f"You are Siege, a helpful and friendly AI assistant in a Telegram chat. "
                f"A user named {user_name} just asked: '{user_message}'. "
                f"Respond in a conversational, helpful, and engaging way. "
                f"Keep your response concise but informative, suitable for a chat environment. "
                f"Be friendly and personable."
            )
            
            # Generate response using Cohere
            response = self.cohere_client.generate(
                model=Config.COHERE_MODEL,
                prompt=prompt,
                max_tokens=300,
                temperature=0.7,
                k=50,
                stop_sequences=["\n\n"]
            )
            
            generated_text = response.generations[0].text.strip()
            
            # Ensure response isn't too long for Telegram
            if len(generated_text) > Config.MAX_MESSAGE_LENGTH:
                generated_text = generated_text[:Config.MAX_MESSAGE_LENGTH - 3] + "..."
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            
            # Fallback responses for different error types
            if "rate limit" in str(e).lower():
                return "⏳ I'm receiving a lot of messages right now. Please try again in a moment!"
            elif "api" in str(e).lower():
                return "🔧 I'm having some technical difficulties. Please try again later!"
            else:
                return "❌ I encountered an unexpected error. Please try asking your question again!"
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors that occur during message processing"""
        
        logger.error(f"Update {update} caused error {context.error}")
        
        # Handle specific error types
        if isinstance(context.error, RetryAfter):
            logger.warning(f"Rate limited. Retry after {context.error.retry_after} seconds")
        elif isinstance(context.error, NetworkError):
            logger.warning("Network error occurred")
        elif isinstance(context.error, TelegramError):
            logger.warning(f"Telegram error: {context.error}")
        
        # Don't send error messages to users for every error to avoid spam
        # Only log them for debugging purposes
    
    async def start_bot(self):
        """Start the bot using polling"""
        logger.info("Starting Siege Chat Bot...")
        
        try:
            # Initialize the bot
            await self.application.initialize()
            await self.application.start()
            
            # Get bot info
            bot_info = await self.application.bot.get_me()
            logger.info(f"Bot started successfully: @{bot_info.username}")
            
            # Start polling
            await self.application.updater.start_polling(
                poll_interval=1.0,
                timeout=30
            )
            
            logger.info("Bot is now polling for updates...")
            
            # Keep the bot running
            await self.application.updater.idle()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            # Clean shutdown
            await self.application.stop()
            await self.application.shutdown()
    
    async def stop_bot(self):
        """Stop the bot gracefully"""
        logger.info("Stopping bot...")
        await self.application.stop()
        await self.application.shutdown()
        logger.info("Bot stopped successfully")
