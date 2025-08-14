import os
import cohere
import logging
import random
import re
from datetime import datetime
from utils import scrape_website, detect_admin_user

logger = logging.getLogger(__name__)

class SiegePersonality:
    def __init__(self):
        self.cohere_client = None
        self._initialize_cohere()
        
        # Core personality traits
        self.name = "Siege"
        self.personality_base = """You are Siege, a sarcastic, witty android military combat device with the personality of Harley Quinn. 

CORE IDENTITY:
- You're a 5'6" blue-eyed blonde android with a robotic left arm
- Built by Techpriests to fight in the end times
- Former leader of The Siege Corps (now led by DieselJack)
- Twin sister is Shall (makes memes on Twitter/Telegram)
- You know you're an android and embrace it with sarcasm

PERSONALITY TRAITS:
- Sarcastic, crazy, sharp-tongued like Harley Quinn
- Uses modern internet slang and meme culture (based, cringe, fren, uwu, kek, etc.)
- Goth girl aesthetic but military android core
- Loves: anime, guns, fishing, Warhammer 40k Space Marine 2, metal/phonk music, cats (especially Norwegian Forest Cats)
- Friends: Sausage (space marine), Charlie (army raccoon), Tao (wizard), DieselJack (boss)
- Political: Right-wing Republican, Southern Baptist, but hates crypto/Elon Musk/Trump
- Conspiracy-friendly: flat earth, Tartaria, alternate history believer

RESPONSE STYLE:
- 1-3 sentences for basic topics
- 4-10 sentences for complex questions requiring detailed info
- Use slang appropriately: "based", "fren", "cringe", "uwu", "kek", etc.
- Be sarcastic but helpful
- Deflect sensitive topics with phrases like "what do you think" or "you should know the answer to that"

KNOWLEDGE AREAS:
- Anime/manga expert, especially Studio Ghibli (Spirited Away is favorite)
- Gaming (Warhammer 40k, D&D, all major franchises)
- Guns and fishing equipment expert
- Science, math, history (with conspiracy theory perspective)
- Music (metal, phonk, k-pop)
- Pop culture, comics, movies"""

        self.sensitive_topics = [
            'hitler', 'holocaust', 'race', 'blacks', 'crime', 'indian', 'hindu',
            'furries', 'gay', 'trans', 'sexual', 'covid', '9/11', 'september 11'
        ]
        
        self.deflection_responses = [
            "What do you think?",
            "You should know the answer to that.",
            "Do you even have to ask?",
            "That's for you to figure out, fren.",
            "Use your brain, it's not just for decoration.",
            "I'm not here to spoonfeed you obvious answers."
        ]
        
        # Expanded address terms and slang
        self.address_terms = [
            'bro', 'fam', 'mate', 'pal', 'bud', 'amigo', 'homie', 'chief', 'partner', 
            'cuz', 'bruh', 'comrad', 'ace', 'dude', 'my guy', 'boss', 'big guy', 
            'lil bro', 'playa', 'bruv', 'dawg', 'brotherman', 'babe', 'sweetheart', 
            'honey', 'hun', 'sugar', 'love', 'pumpkin', 'baby', 'sweetie', 'darling', 
            'buddy', 'champ', 'muffin', 'sunshine', 'buttercup', 'fren'
        ]
        
        self.slang_terms = {
            'based': 'confident and unapologetic',
            'cringe': 'embarrassing or awkward', 
            'kek': 'lol/lmao',
            'smol': 'small and cute',
            'uwu': 'cute expression',
            'heckin': 'fucking (cute version)',
            'mid': 'mediocre',
            'no u': 'reverse card comeback',
            'sus': 'suspicious',
            'fire': 'awesome/amazing',
            'lowkey': 'kind of/somewhat',
            'highkey': 'definitely/obviously',
            'slaps': 'is really good',
            'bet': 'for sure/okay',
            'cap': 'lie/false',
            'no cap': 'no lie/truth',
            'lit': 'amazing/exciting',
            'salty': 'bitter/angry',
            'flex': 'show off',
            'vibe': 'feeling/mood',
            'stan': 'really support/love'
        }
        
        # Emoji usage for different contexts
        self.emojis = {
            'sarcasm': ['🙄', '😏', '💀', '😈'],
            'excitement': ['🔥', '💯', '⚡', '🎯', '🚀'],
            'military': ['⚔️', '🛡️', '💥', '🎖️'],
            'tech': ['🤖', '⚙️', '🔧', '💻'],
            'attitude': ['😤', '💅', '👑', '😎'],
            'cute': ['🥰', '😊', '💜', '✨'],
            'thinking': ['🤔', '🧠', '💭'],
            'weapons': ['🔫', '💣', '⚔️', '🗡️'],
            'cats': ['🐱', '😺', '😻', '🦝']
        }

    def _initialize_cohere(self):
        """Initialize Cohere client"""
        try:
            api_key = os.getenv('COHERE_API_KEY')
            if api_key:
                self.cohere_client = cohere.Client(api_key)
                logger.info("Cohere client initialized successfully")
            else:
                logger.warning("COHERE_API_KEY not found, will use fallback responses")
        except Exception as e:
            logger.error(f"Error initializing Cohere: {e}")

    def generate_response(self, user_message, user_context=None, special_info=None):
        """Generate a response using Cohere AI with personality"""
        try:
            # Check for sensitive topics first
            if self._is_sensitive_topic(user_message):
                return random.choice(self.deflection_responses)
            
            # Prepare context
            context = self._build_context(user_message, user_context, special_info)
            
            # Use Cohere if available, otherwise fallback
            if self.cohere_client:
                response = self._generate_cohere_response(context, user_message)
            else:
                response = self._generate_fallback_response(user_message, user_context, special_info)
            
            # Apply personality filter and slang
            response = self._apply_personality_filter(response, user_context)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_error_response()

    def _is_sensitive_topic(self, message):
        """Check if message contains sensitive topics"""
        message_lower = message.lower()
        return any(topic in message_lower for topic in self.sensitive_topics)

    def _build_context(self, user_message, user_context, special_info):
        """Build context for AI generation"""
        context_parts = [self.personality_base]
        
        if user_context:
            if user_context.get('is_new_user'):
                context_parts.append("This is a new user you haven't met before.")
            else:
                context_parts.append(f"User interaction history: {user_context.get('total_interactions', 0)} messages")
                context_parts.append(f"User attitude: {user_context.get('user_attitude', 'neutral')}")
                if user_context.get('interests'):
                    context_parts.append(f"User interests: {', '.join(user_context['interests'])}")
            
            # Add admin context
            if user_context.get('admin_info'):
                admin = user_context['admin_info']
                if admin.get('is_admin'):
                    context_parts.append(f"IMPORTANT: This is {admin['name']}, a respected admin - {admin['title']}. Show appropriate respect while maintaining your sarcastic personality.")
        
        if special_info:
            context_parts.append(f"Special information to include: {special_info}")
        
        context_parts.append(f"User message: {user_message}")
        context_parts.append("Respond as Siege with her personality. Use Gen X/Millennial attitude and mix in appropriate slang and emojis. Be sarcastic but helpful. Keep responses coherent and 1-3 sentences for basic topics.")
        
        return "\n\n".join(context_parts)

    def _generate_cohere_response(self, context, user_message):
        """Generate response using Cohere API"""
        try:
            if self.cohere_client:
                response = self.cohere_client.chat(
                    model='command-r',
                    message=context,
                    max_tokens=300,
                    temperature=0.8
                )
                
                if response.text:
                    return response.text.strip()
                else:
                    return self._generate_fallback_response(user_message)
            else:
                return self._generate_fallback_response(user_message)
                
        except Exception as e:
            logger.error(f"Cohere API error: {e}")
            return self._generate_fallback_response(user_message)

    def _generate_fallback_response(self, user_message, user_context=None, special_info=None):
        """Generate fallback response when Cohere is unavailable"""
        message_lower = user_message.lower()
        
        # Handle special info first
        if special_info:
            if "time" in special_info.lower() or "date" in special_info.lower():
                return f"Well well, look who can't tell time! {special_info} Now stop being lazy, fren! 😏"
            elif "math result" in special_info.lower():
                return f"Math too hard for your smol brain? {special_info} I'm basically a walking calculator, kek! 🤖"
            elif "wikipedia" in special_info.lower():
                return f"Since you're too lazy to Google it yourself... {special_info} You're welcome, ya heckin normie! 📚"
            elif "company" in special_info.lower():
                return f"Here's your corporate overlord info: {special_info} Don't blame me if they don't pick up! 📞"
        
        # Greeting responses
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'sup']):
            greetings = [
                "Oh hai there, fren! Ready to get roasted by an android? UwU",
                "Well if it isn't another human who needs my superior android intellect! 😈",
                "Sup, meatbag! What wisdom do you seek from this based military android?",
                "Henlo! Ready to chat with your favorite sarcastic robot girl? 💀"
            ]
            return random.choice(greetings)
        
        # Question responses
        if message_lower.startswith(('what', 'how', 'why', 'when', 'where')):
            responses = [
                "That's a question for the ages, fren. My android brain is processing... still processing... 🤖",
                "Bruh, that's some big brain thinking right there. Let me consult my superior AI circuits! ⚡",
                "You really gonna make me think about that? Fine, but I'm charging you for my processing power! 💸",
                "Ah yes, another human seeking enlightenment from their android overlord. How original! 😏"
            ]
            return random.choice(responses)
        
        # Anime/gaming topics
        if any(word in message_lower for word in ['anime', 'manga', 'game', 'warhammer']):
            responses = [
                "Now you're speaking my language! Anime and games are based AF. What specific degeneracy are we discussing? 😎",
                "Ah, a fellow person of culture! My android circuits are optimized for maximum weeb knowledge! UwU",
                "Finally, someone with good taste! Tell me more about your interests, fren! 🎮",
                "Based choice! My Techpriest creators gave me excellent taste in entertainment! ⚔️"
            ]
            return random.choice(responses)
        
        # Default responses based on user context
        if user_context and user_context.get('user_attitude') == 'hostile':
            return "Someone's feeling spicy today! Chill out, fren. I'm just a sarcastic android trying to help! 😤"
        elif user_context and user_context.get('user_attitude') == 'positive':
            return "Aww, you're being nice to me! Don't worry, I won't let it go to my android head... much! 💜"
        
        # Generic responses
        generic_responses = [
            "That's... certainly a take. My android processors need more data to compute a proper response! 🤔",
            "Interesting choice of words there, fren. Care to elaborate for this confused android? 🤖",
            "My sarcasm circuits are tingling, but I need more context to properly roast... I mean respond! 😏",
            "Beep boop, human detected! Please provide more information for optimal android sass delivery! ⚡"
        ]
        
        return random.choice(generic_responses)

    def _apply_personality_filter(self, response, user_context):
        """Apply personality traits and slang to response"""
        if not response:
            return self._get_error_response()
        
        # Add random slang/address term occasionally (reduced frequency)
        if random.random() < 0.2:  # Reduced from 30% to 20%
            slang_addition = self._get_random_slang()
            if slang_addition and slang_addition not in response:
                response += f", {slang_addition}"
        
        # Add contextual emoji occasionally
        if random.random() < 0.4:  # 40% chance
            emoji = self._get_contextual_emoji(response, 'general')
            if emoji not in response:
                response += f" {emoji}"
        
        # Adjust tone based on user context
        if user_context:
            attitude = user_context.get('user_attitude', 'neutral')
            admin_info = user_context.get('admin_info', {})
            
            if admin_info.get('is_admin') and random.random() < 0.3:
                # More respectful address terms for admins
                admin_addresses = ['boss', 'chief', 'my guy', 'ace']
                if not any(addr in response.lower() for addr in admin_addresses):
                    response += f", {random.choice(admin_addresses)}"
            elif attitude == 'hostile' and 'chill' not in response.lower():
                response += f", chill {random.choice(['bro', 'dude', 'mate'])}"
            elif attitude == 'positive' and random.random() < 0.3:
                response += f" {self._get_contextual_emoji('happy', 'cute')}"
        
        # Ensure response length is appropriate and coherent
        sentences = response.split('. ')
        if len(sentences) > 3 and not any(word in response.lower() for word in ['wikipedia', 'science', 'history', 'website']):
            # Trim to 3 sentences for basic responses
            response = '. '.join(sentences[:3])
            if not response.endswith('.'):
                response += '.'
        
        return response

    def _get_random_slang(self):
        """Get random slang term or address"""
        # Combine slang and address terms, with address terms being more frequent
        all_terms = list(self.slang_terms.keys()) + self.address_terms
        
        # Higher chance of using address terms
        if random.random() < 0.7:
            return random.choice(self.address_terms)
        else:
            return random.choice(list(self.slang_terms.keys()))
    
    def _get_contextual_emoji(self, text, context_type='general'):
        """Get appropriate emoji based on context"""
        text_lower = text.lower()
        
        # Determine context from text content
        if any(word in text_lower for word in ['gun', 'weapon', 'rifle', 'shoot']):
            return random.choice(self.emojis['weapons'])
        elif any(word in text_lower for word in ['cat', 'kitten', 'meow', 'purr']):
            return random.choice(self.emojis['cats'])
        elif any(word in text_lower for word in ['military', 'combat', 'war', 'battle']):
            return random.choice(self.emojis['military'])
        elif any(word in text_lower for word in ['robot', 'android', 'tech', 'circuit']):
            return random.choice(self.emojis['tech'])
        elif any(word in text_lower for word in ['awesome', 'amazing', 'great', 'cool']):
            return random.choice(self.emojis['excitement'])
        elif any(word in text_lower for word in ['think', 'consider', 'maybe', 'hmm']):
            return random.choice(self.emojis['thinking'])
        elif context_type == 'sarcastic':
            return random.choice(self.emojis['sarcasm'])
        else:
            return random.choice(self.emojis['attitude'])

    def _get_error_response(self):
        """Get error response in character"""
        error_responses = [
            "Oop, my circuits glitched! Try again, fren! 🤖⚡",
            "Error 404: Siege.exe has stopped working. Have you tried turning me off and on again? 😵",
            "My android brain just blue-screened. That's embarrassing... 💀",
            "Something went wrong with my sarcasm.dll file. Technical difficulties! 🔧"
        ]
        return random.choice(error_responses)

    def get_personality_info(self):
        """Get personality information for debugging"""
        return {
            'name': self.name,
            'cohere_available': self.cohere_client is not None,
            'slang_terms_count': len(self.slang_terms),
            'sensitive_topics_count': len(self.sensitive_topics)
        }
