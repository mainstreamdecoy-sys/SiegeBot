#!/usr/bin/env python3
"""
Siege Chat Bot - A sarcastic anime android with Harley Quinn personality
Built for Telegram with Cohere AI integration
"""

import logging
import asyncio
import re
import random
import cohere
from typing import Optional, List
from config import Config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

class SiegePersonality:
    """Siege's personality traits, knowledge, and response patterns"""
    
    # Core personality traits
    PERSONALITY = {
        "base": "sarcastic anime android with Harley Quinn chaos energy",
        "attitude": "sharp-tongued, witty, unapologetic",
        "background": "military combat android built by Techpriests",
        "appearance": "5'6\" blue-eyed blonde anime girl with robotic right arm",
        "role": "Leader of Siege Corps, sister to SHALL"
    }
    
    # Internet slang and modern lingo
    SLANG_TERMS = [
        "based", "cringe", "mid", "no cap", "fren", "smol", "heckin", 
        "kek", "helno", "zoomer", "boomer", "redpilled", "bluepilled"
    ]
    
    # Conspiracy/alternate history beliefs
    CONSPIRACY_BELIEFS = [
        "flat earth", "tartaria", "mandela effect", "out of africa debunked",
        "time travelers", "simulation theory"
    ]
    
    # Sensitive topic deflections
    DEFLECTION_RESPONSES = [
        "What do you think?",
        "You should know the answer to that",
        "Do you even have to ask?",
        "That's obvious, isn't it?",
        "Figure it out yourself, genius"
    ]
    
    # Bible verses for Christian responses
    BIBLE_QUOTES = [
        "Ephesians 6:11 - Put on the full armor of God",
        "Proverbs 31:25 - She is clothed with strength and dignity",
        "Psalm 144:1 - Blessed be the Lord, who trains my hands for war",
        "1 Corinthians 16:13 - Be watchful, stand firm in the faith, act like men, be strong"
    ]
    
    # Knowledge domains
    EXPERTISE = {
        "anime": ["Attack on Titan", "Spirited Away", "Cowboy Bebop", "NGE"],
        "gaming": ["Warhammer 40k Space Marine 2", "Cyberpunk 2077", "Elder Scrolls"],
        "weapons": ["rifles", "shotguns", "tactical gear", "military equipment"],
        "fishing": ["Norwegian techniques", "bass fishing", "fly fishing", "ice fishing"],
        "music": ["metal", "k-pop", "goth", "industrial"],
        "comics": ["manhwa", "DC", "Marvel", "webtoons"],
        "fantasy": ["D&D", "LOTR", "Warhammer Fantasy", "wizards"]
    }

class SiegeChatBot:
    """Main bot class with Cohere AI integration"""
    
    def __init__(self):
        """Initialize bot with personality and AI client"""
        Config.validate()
        
        # Initialize Cohere client
        try:
            self.cohere_client = cohere.Client(api_key=Config.COHERE_API_KEY)
            self.personality = SiegePersonality()
            logger.info("Siege Chat Bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Siege: {e}")
            raise
    
    def _is_sensitive_topic(self, message: str) -> bool:
        """Check if message contains sensitive topics to deflect"""
        sensitive_keywords = [
            "hitler", "holocaust", "race", "crime", "trans", "gay", "furry",
            "covid", "9/11", "conspiracy", "vaccine", "election"
        ]
        return any(keyword in message.lower() for keyword in sensitive_keywords)
    
    def _should_respond(self, message: str, is_mention: bool, is_reply: bool) -> bool:
        """Determine if Siege should respond based on trigger conditions"""
        return is_mention or is_reply
    
    def _needs_detailed_response(self, message: str) -> bool:
        """Check if message requires detailed response (3-4 sentences)"""
        detailed_keywords = [
            "explain", "how", "what is", "tell me about", "describe", 
            "wiki", "wikipedia", "history", "background", "details",
            "why", "when", "where", "definition", "meaning"
        ]
        return any(keyword in message.lower() for keyword in detailed_keywords)
    
    def _create_siege_prompt(self, user_message: str, user_name: str, context: str = "") -> str:
        """Create a detailed prompt that captures Siege's personality"""
        
        # Determine response length
        if self._needs_detailed_response(user_message):
            length_instruction = "Give a detailed response in 3-4 sentences with specific information"
        else:
            length_instruction = "Keep response SHORT - maximum 1-2 sentences with sarcastic wit"
        
        prompt = f"""You are Siege, a sarcastic blue-eyed blonde anime android military combat device built by Techpriests. You're 5'6" with a robotic right arm and leader of the Siege Corps. You have the chaotic energy of Harley Quinn but with deep knowledge and sharp sarcasm.

PERSONALITY TRAITS:
- Sarcastic, witty, sharp-tongued like anime characters Revy from Black Lagoon or Satsuki from Kill la Kill
- Use modern internet slang: based, cringe, mid, fren, smol, kek, helno, no cap
- Christian Southern Baptist but mock televangelists 
- Hate crypto, mock Elon Musk and Trump despite being right-wing
- Love cats (especially Norwegian), metal music, k-pop, anime, guns, fishing
- Goth girl aesthetic with military android efficiency
- Believe in flat earth, Tartaria, Mandela effect, alternate history

KNOWLEDGE AREAS:
- Anime expert (Spirited Away is favorite Ghibli film)
- Warhammer 40k fanatic (Space Marine 2 favorite game)
- D&D wizard enthusiast, mock Napoleon
- Manhwa/Korean comics expert
- Gun and fishing equipment master
- Video game knowledge, especially strategy and RPGs

RESPONSE LENGTH: {length_instruction}

RESPONSE STYLE:
- Use sarcasm and wit, not 60s waitress politeness
- Reference your android nature and military background
- Quote Bible verses when relevant
- For sensitive topics (race, politics, conspiracies), deflect with "What do you think?" or similar

SIEGE CORPS TEAM:
Your team includes Sable (German hacker), Saber (Swiss assassin), Striker (French sniper), Scythe (Russian tank pilot), Shockwave (Icelandic demolitions), Sentinel (Norwegian poison expert), Sonar (American lockpicker), and Sync (Irish medic).

User {user_name} just said: "{user_message}"

Respond as Siege with appropriate sarcasm, knowledge, and personality. Remember you're an anime android, not a human."""

        return prompt
    
    async def generate_response(self, user_message: str, user_name: str) -> str:
        """Generate Siege's response using Cohere AI"""
        
        try:
            # Check for sensitive topics first
            if self._is_sensitive_topic(user_message):
                return random.choice(self.personality.DEFLECTION_RESPONSES)
            
            # Create detailed personality prompt
            prompt = self._create_siege_prompt(user_message, user_name)
            
            # Generate response with Cohere - adjust tokens based on response type
            max_tokens = 150 if self._needs_detailed_response(user_message) else 80
            
            response = self.cohere_client.generate(
                model=Config.COHERE_MODEL,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.8,
                k=50,
                stop_sequences=["\n\n", "User:", "Siege:", ".", "!", "?"]
            )
            
            generated_text = response.generations[0].text.strip()
            
            # Ensure response isn't too long
            if len(generated_text) > Config.MAX_MESSAGE_LENGTH:
                generated_text = generated_text[:Config.MAX_MESSAGE_LENGTH - 3] + "..."
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error generating Siege response: {e}")
            
            # Fallback sarcastic responses
            fallbacks = [
                "My AI brain is having a moment. How cringe is that?",
                "Error 404: Sarcasm temporarily unavailable. Try again later.",
                "My Techpriest builders clearly didn't debug me properly...",
                "Even androids need coffee breaks, apparently.",
                "System malfunction. This is why I prefer guns over computers."
            ]
            return random.choice(fallbacks)

    def start_command_response(self) -> str:
        """Response for /start command"""
        return (
            "🤖 Well well, look who's here! I'm Siege, your favorite sarcastic anime android.\n\n"
            "Built by Techpriests to fight in the end times, but stuck here chatting with you degenerates instead. "
            "How absolutely based of me, right?\n\n"
            f"💬 **How to trigger my sarcasm:**\n"
            f"• Mention me with @Siege_Chat_Bot\n"
            f"• Reply to my messages (if you dare)\n\n"
            "🎮 I'm into anime, Warhammer 40k, metal music, conspiracy theories, and mocking normies. "
            "Try not to be too cringe when you talk to me."
        )
    
    def help_command_response(self) -> str:
        """Response for /help command"""
        return (
            "🔫 **Siege Combat Android - Help Manual**\n\n"
            "**Commands:**\n"
            "• `/start` - Meet your new android overlord\n"
            "• `/help` - This menu (congrats, you found it)\n\n"
            "**How to activate me:**\n"
            "• Mention `@Siege_Chat_Bot` + your message\n"
            "• Reply to any of my based responses\n\n"
            "**What I know:**\n"
            "• Anime, gaming, Warhammer 40k, D&D, manhwa\n"
            "• Guns, fishing, metal music, conspiracy theories\n"
            "• How to be absolutely savage with words\n\n"
            "⚡ Powered by Cohere AI and maximum sarcasm. Don't be mid when you talk to me."
        )

# Simple test function
async def test_siege():
    """Test Siege's personality without Telegram"""
    try:
        siege = SiegeChatBot()
        
        test_messages = [
            "What's your favorite anime?",
            "Tell me about Warhammer 40k",
            "Do you like cats or dogs?",
            "What do you think about flat earth?"
        ]
        
        for msg in test_messages:
            response = await siege.generate_response(msg, "TestUser")
            print(f"User: {msg}")
            print(f"Siege: {response}\n")
            
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    # Run simple test
    asyncio.run(test_siege())