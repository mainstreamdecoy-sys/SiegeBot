import os
import requests
import json
import logging
import random
from datetime import datetime, timedelta
from app import db
from models import UserInteraction, GroupChat, BotMemory
from personality import SiegePersonality
from utils import get_current_time, search_wikipedia, calculate_math, get_company_info, scrape_website, detect_admin_user

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.bot_username = 'Siege_Chat_Bot'
        self.api_url = f"https://api.telegram.org/bot{self.token}"
        self.personality = SiegePersonality()
        self.last_message_time = {}  # Track last message time per chat
        self.message_count = {}  # Track message count per chat per minute
        
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
            raise ValueError("Telegram bot token is required")
    
    def get_bot_info(self):
        """Get bot information"""
        try:
            response = requests.get(f"{self.api_url}/getMe")
            return response.json()
        except Exception as e:
            logger.error(f"Error getting bot info: {e}")
            return None
    
    def set_webhook(self, webhook_url):
        """Set webhook URL"""
        try:
            response = requests.post(f"{self.api_url}/setWebhook", 
                                   json={"url": webhook_url})
            return response.json()
        except Exception as e:
            logger.error(f"Error setting webhook: {e}")
            return None
    
    def send_message(self, chat_id, text, reply_to_message_id=None):
        """Send a message to a chat with error handling"""
        try:
            data = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML"
            }
            
            if reply_to_message_id:
                data["reply_to_message_id"] = reply_to_message_id
            
            response = requests.post(f"{self.api_url}/sendMessage", json=data, timeout=10)
            response_data = response.json()
            
            # Check for rate limit errors
            if not response_data.get('ok'):
                error_code = response_data.get('error_code')
                if error_code == 429:  # Too Many Requests
                    logger.warning(f"Rate limited for chat {chat_id}")
                    return None
                elif error_code == 400:  # Bad Request (often means bot was blocked)
                    logger.warning(f"Bot blocked or bad request for chat {chat_id}")
                    return None
                else:
                    logger.error(f"Telegram API error {error_code}: {response_data.get('description')}")
                    return None
            
            return response_data
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout sending message to chat {chat_id}")
            return None
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return None
    
    def process_update(self, update):
        """Process incoming update from Telegram"""
        try:
            if 'message' not in update:
                return
            
            message = update['message']
            chat_id = message['chat']['id']
            user = message.get('from', {})
            user_id = user.get('id')
            text = message.get('text', '')
            message_id = message.get('message_id')
            
            # Update group chat info
            self._update_group_chat(message['chat'])
            
            # Determine if we should respond
            should_respond = self._should_respond(message)
            
            if should_respond:
                response_text = self._generate_response(message)
                
                if response_text:
                    # Send response
                    result = self.send_message(chat_id, response_text, message_id)
                    
                    # Only store interaction if message was sent successfully
                    if result and result.get('ok'):
                        self._store_interaction(user, chat_id, text, response_text, 
                                              self._get_message_type(message))
                        logger.info(f"Responded to {user.get('username', user_id)} in chat {chat_id}")
                    else:
                        logger.warning(f"Failed to send response to {user.get('username', user_id)} in chat {chat_id}")
        
        except Exception as e:
            logger.error(f"Error processing update: {e}")
    
    def _should_respond(self, message):
        """Determine if bot should respond to message with rate limiting"""
        chat_id = message['chat']['id']
        text = message.get('text', '').lower()
        chat_type = message['chat']['type']
        
        # Check rate limits
        if not self._check_rate_limit(chat_id):
            logger.info(f"Rate limit exceeded for chat {chat_id}")
            return False
        
        # Always respond to commands (but with rate limit)
        if text.startswith('/'):
            return True
        
        # Always respond to mentions (but with rate limit)
        if f'@{self.bot_username.lower()}' in text:
            return True
        
        # Always respond to replies to bot messages (but with rate limit)
        reply_to = message.get('reply_to_message')
        if reply_to and reply_to.get('from', {}).get('username') == self.bot_username:
            return True
        
        # Always respond in private chats (but with rate limit)
        if chat_type == 'private':
            return True
        
        # Disable random responses in groups completely to prevent spam
        # if chat_type in ['group', 'supergroup']:
        #     return False  # No random responses
        
        return False
    
    def _check_rate_limit(self, chat_id):
        """Check if we're within rate limits for this chat"""
        now = datetime.now()
        
        # Initialize tracking for new chats
        if chat_id not in self.last_message_time:
            self.last_message_time[chat_id] = now
            self.message_count[chat_id] = 1
            return True
        
        # Reset counter if more than 1 minute has passed
        if now - self.last_message_time[chat_id] > timedelta(minutes=1):
            self.message_count[chat_id] = 1
            self.last_message_time[chat_id] = now
            return True
        
        # Check if under limit (max 3 messages per minute per chat)
        if self.message_count[chat_id] < 3:
            self.message_count[chat_id] += 1
            self.last_message_time[chat_id] = now
            return True
        
        return False
    
    def _generate_response(self, message):
        """Generate response using personality and context"""
        try:
            text = message.get('text', '')
            user = message.get('from', {})
            chat_id = message['chat']['id']
            
            # Handle commands
            if text.startswith('/start'):
                return self._handle_start_command(user)
            elif text.startswith('/help'):
                return self._handle_help_command()
            
            # Get user context
            user_context = self._get_user_context(user.get('id'), chat_id, 
                                                 user.get('username'), user.get('first_name'))
            
            # Handle special requests
            if any(keyword in text.lower() for keyword in ['time', 'date', 'year']):
                time_info = get_current_time()
                return self.personality.generate_response(text, user_context, 
                                                        special_info=time_info)
            
            # Handle math questions
            if any(keyword in text.lower() for keyword in ['calculate', 'math', '+', '-', '*', '/', '=']):
                math_result = calculate_math(text)
                if math_result:
                    return self.personality.generate_response(text, user_context, 
                                                            special_info=f"Math result: {math_result}")
            
            # Handle Wikipedia searches
            if any(keyword in text.lower() for keyword in ['wikipedia', 'what is', 'who is', 'tell me about']):
                wiki_info = search_wikipedia(text)
                if wiki_info:
                    return self.personality.generate_response(text, user_context, 
                                                            special_info=wiki_info)
            
            # Handle company info requests
            if any(keyword in text.lower() for keyword in ['phone number', 'address', 'company', 'business']):
                company_info = get_company_info(text)
                if company_info:
                    return self.personality.generate_response(text, user_context, 
                                                            special_info=company_info)
            
            # Handle website scraping requests
            if any(keyword in text.lower() for keyword in ['read', 'check', 'look at', 'scrape', 'website', 'article', 'news']):
                # Look for URLs in the message
                import re
                urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
                if urls:
                    scraped_content = scrape_website(urls[0])
                    if scraped_content:
                        return self.personality.generate_response(text, user_context, 
                                                                special_info=f"Website content: {scraped_content}")
                    else:
                        return self.personality.generate_response(text, user_context, 
                                                                special_info="Sorry boss, I can't access that website - either it's restricted or having issues.")
            
            # Generate regular personality response
            return self.personality.generate_response(text, user_context)
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Something went wrong with my circuits. Try again, fren!"
    
    def _handle_start_command(self, user):
        """Handle /start command"""
        name = user.get('first_name', 'unknown')
        return (f"Well well, look who's here! Hey there {name}! 💀\n"
                f"I'm Siege, your friendly neighborhood android with a twisted sense of humor. "
                f"Built by Techpriests to fight the good fight, but here I am chatting with you degenerates instead! "
                f"Mention me with @{self.bot_username} or reply to my messages if you want to chat. "
                f"Fair warning - I'm sarcastic AF and have opinions about everything! UwU")
    
    def _handle_help_command(self):
        """Handle /help command"""
        return (f"🤖 <b>Siege Bot Commands & Features</b>\n\n"
                f"<b>How to interact:</b>\n"
                f"• Mention me: @{self.bot_username} your message\n"
                f"• Reply to my messages\n"
                f"• Use commands: /start, /help\n\n"
                f"<b>What I can do:</b>\n"
                f"• Answer questions with Cohere AI\n"
                f"• Tell current time/date\n"
                f"• Solve math problems\n"
                f"• Search Wikipedia for facts\n"
                f"• Find company info\n"
                f"• Remember our conversations\n"
                f"• Be sarcastic and based 24/7\n\n"
                f"I'm an anime military android with a Harley Quinn attitude. "
                f"Ask me about games, anime, guns, fishing, or anything really! "
                f"Just don't expect me to be nice about it~ 😈")
    
    def _get_message_type(self, message):
        """Determine message type"""
        text = message.get('text', '')
        
        if text.startswith('/'):
            return 'command'
        elif f'@{self.bot_username}' in text:
            return 'mention'
        elif message.get('reply_to_message'):
            return 'reply'
        else:
            return 'random'
    
    def _get_user_context(self, user_id, chat_id, username=None, first_name=None):
        """Get user context for personality adaptation"""
        if not user_id:
            return {}
        
        # Get recent interactions
        interactions = UserInteraction.query.filter_by(
            user_id=user_id, chat_id=chat_id
        ).order_by(UserInteraction.timestamp.desc()).limit(10).all()
        
        # Detect admin status
        admin_info = detect_admin_user(username, first_name)
        
        if not interactions:
            context = {'is_new_user': True}
            if admin_info and isinstance(admin_info, dict) and admin_info.get('is_admin'):
                context['admin_info'] = admin_info
            return context
        
        # Analyze user behavior
        latest = interactions[0]
        total_interactions = len(interactions)
        
        # Get interests
        interests = latest.get_interests_list() if latest.interests else []
        
        context = {
            'is_new_user': False,
            'total_interactions': total_interactions,
            'user_attitude': latest.user_attitude or 'neutral',
            'interests': interests,
            'last_interaction': latest.timestamp
        }
        
        if admin_info and isinstance(admin_info, dict) and admin_info.get('is_admin'):
            context['admin_info'] = admin_info
        
        return context
    
    def _store_interaction(self, user, chat_id, message_text, bot_response, message_type):
        """Store user interaction in database"""
        try:
            # Check if user exists
            user_id = user.get('id')
            if not user_id:
                return
            
            existing = UserInteraction.query.filter_by(
                user_id=user_id, chat_id=chat_id
            ).order_by(UserInteraction.timestamp.desc()).first()
            
            # Detect interests and attitude
            interests = self._detect_interests(message_text)
            attitude = self._detect_attitude(message_text)
            
            if existing:
                # Update existing user's interests and attitude
                existing_interests = existing.get_interests_list()
                combined_interests = list(set(existing_interests + interests))
                existing.set_interests_list(combined_interests)
                existing.user_attitude = attitude
                existing.interaction_count += 1
            
            # Create new interaction record
            interaction = UserInteraction()
            interaction.user_id = user_id
            interaction.username = user.get('username')
            interaction.first_name = user.get('first_name')
            interaction.chat_id = chat_id
            interaction.message_text = message_text
            interaction.bot_response = bot_response
            interaction.message_type = message_type
            interaction.user_attitude = attitude
            interaction.interests = json.dumps(interests)
            
            db.session.add(interaction)
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error storing interaction: {e}")
            db.session.rollback()
    
    def _update_group_chat(self, chat_info):
        """Update group chat information"""
        try:
            chat_id = chat_info['id']
            existing = GroupChat.query.filter_by(chat_id=chat_id).first()
            
            if existing:
                existing.last_activity = datetime.utcnow()
                existing.chat_title = chat_info.get('title')
            else:
                group_chat = GroupChat()
                group_chat.chat_id = chat_id
                group_chat.chat_title = chat_info.get('title')
                group_chat.chat_type = chat_info.get('type')
                group_chat.last_activity = datetime.utcnow()
                db.session.add(group_chat)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error updating group chat: {e}")
            db.session.rollback()
    
    def _detect_interests(self, text):
        """Detect user interests from message text"""
        interests = []
        text_lower = text.lower()
        
        # Interest keywords mapping
        interest_keywords = {
            'anime': ['anime', 'manga', 'waifu', 'otaku', 'spirited away', 'ghibli'],
            'gaming': ['game', 'gaming', 'warhammer', 'fps', 'mmo', 'pc gaming'],
            'guns': ['gun', 'rifle', 'pistol', 'shooting', 'firearms'],
            'fishing': ['fishing', 'fish', 'rod', 'tackle', 'bait'],
            'music': ['music', 'metal', 'phonk', 'goth', 'band'],
            'conspiracy': ['conspiracy', 'flat earth', 'mandela effect', 'tartaria'],
            'science': ['science', 'physics', 'chemistry', 'biology', 'math'],
            'history': ['history', 'napoleon', 'ancient', 'medieval']
        }
        
        for interest, keywords in interest_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                interests.append(interest)
        
        return interests
    
    def _detect_attitude(self, text):
        """Detect user attitude from message text"""
        text_lower = text.lower()
        
        # Positive indicators
        positive_words = ['good', 'great', 'awesome', 'cool', 'nice', 'thanks', 'love']
        # Negative indicators
        negative_words = ['bad', 'sucks', 'hate', 'stupid', 'dumb', 'awful']
        # Hostile indicators
        hostile_words = ['fuck', 'shit', 'stupid bot', 'stfu', 'shut up']
        
        if any(word in text_lower for word in hostile_words):
            return 'hostile'
        elif any(word in text_lower for word in negative_words):
            return 'negative'
        elif any(word in text_lower for word in positive_words):
            return 'positive'
        else:
            return 'neutral'
