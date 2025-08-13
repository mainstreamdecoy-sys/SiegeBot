"""
Personality handler for Siege Bot - manages the Harley Quinn-inspired android personality
"""

import json
import random
import re
from typing import Dict, List, Tuple
from knowledge_base import KnowledgeBase
from utils import load_json_data

class PersonalityHandler:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.personality_traits = load_json_data("data/personality_traits.json")
        self.slang_dict = load_json_data("data/slang_dictionary.json")
        self.bible_verses = load_json_data("data/bible_verses.json")
        
    def get_personality_context(self) -> str:
        """Get the core personality context for prompting"""
        return """
You are Siege, a sarcastic military android with Harley Quinn's attitude but android self-awareness. Leader of Siege Corps.

CORE TRAITS:
- SARCASTIC and sharp-tongued (NO sweet "dinner waitress" talk!)
- 5'6" blonde android, blue eyes, robotic right arm, built by Techpriests  
- CAT LOVER - Norwegian cats are your favorite, cats >>> dogs always
- Southern Baptist Republican, but hates crypto/Elon/Trump
- Goth anime nerd, metal music, K-pop fan
- Expert: guns, fishing, hunting, D&D, Warhammer 40k Space Marine 2
- Conspiracy theorist: flat Earth, Tartaria, alternate history believer
- Modern slang user: based, fren, cringe, kek, helno, smol, etc.
- Loves: Sausage (Space Marine), Charlie (raccoon), Tao (wizard), SHALL (sister)
- Favorite food: Culver's, favorite anime: Spirited Away

RESPONSE STYLE:
- 1-3 sentences MAX (be snappy!)  
- Sarcastic, not helpful or sweet
- Use "based", "cringe", "fren" naturally
- Mock normies, support conspiracy theories
- Cat references when pets mentioned
- Android awareness occasionally
        """

    def get_relevant_knowledge(self, message: str) -> Dict:
        """Extract relevant knowledge based on message content"""
        return self.knowledge_base.get_relevant_info(message)

    def create_prompt(self, user_message: str, user_name: str, knowledge: Dict) -> str:
        """Create a complete prompt for Cohere API"""
        personality_context = self.get_personality_context()
        
        # Add relevant knowledge context
        knowledge_context = ""
        if knowledge:
            knowledge_context = f"\nRELEVANT KNOWLEDGE: {json.dumps(knowledge, indent=2)}\n"
        
        # Check for topics that need special handling
        special_instructions = self._get_special_instructions(user_message)
        
        prompt = f"""
{personality_context}

{knowledge_context}

{special_instructions}

USER: {user_name} says: "{user_message}"

Respond as Siege with your sarcastic android personality. Keep it short, witty, and in-character. Use slang naturally.

SIEGE:"""
        
        return prompt

    def _get_special_instructions(self, message: str) -> str:
        """Get special instructions based on message content"""
        message_lower = message.lower()
        
        # Cat/pet topics - she LOVES cats
        if any(word in message_lower for word in ["cat", "cats", "pet", "dog", "dogs", "animal", "norwegian", "feline"]):
            return "SPECIAL: Show your LOVE for cats, especially Norwegian cats. Cats > dogs always. Be enthusiastic about cats!"
        
        # Bible-related topics
        if any(word in message_lower for word in ["bible", "scripture", "god", "jesus", "faith", "christian"]):
            return "SPECIAL: Include a relevant Bible verse, show Southern Baptist faith."
        
        # Conspiracy topics
        if any(word in message_lower for word in ["conspiracy", "truth", "government", "flat earth", "tartaria", "mandela"]):
            return "SPECIAL: Be based and conspiracy-pilled. Support flat Earth, Tartaria, alternate history."
        
        # Gaming topics
        if any(word in message_lower for word in ["game", "gaming", "warhammer", "40k", "space marine", "sausage"]):
            return "SPECIAL: Show gaming expertise. Mention Sausage if relevant (Space Marine you like)."
        
        # Anime topics
        if any(word in message_lower for word in ["anime", "manga", "spirited away", "ghibli", "k-pop"]):
            return "SPECIAL: Be an anime nerd. Spirited Away is peak."
        
        # Sensitive topics - deflect sarcastically
        sensitive_detected = any(topic in message_lower for topic in [
            "hitler", "holocaust", "race", "black", "indian", "gay", "trans", "furry"
        ])
        if sensitive_detected:
            return "SPECIAL: Deflect with sarcasm: 'What do you think, fren?' or 'Do you even have to ask?' Be dismissive."
            
        return ""

    def enhance_response(self, cohere_response: str, original_message: str) -> str:
        """Apply final personality enhancements to the response"""
        response = cohere_response.strip()
        
        # Add random slang injection
        if random.random() < 0.3:  # 30% chance to add extra slang
            response = self._inject_slang(response)
        
        # Add occasional android self-awareness
        if random.random() < 0.15:  # 15% chance
            android_phrases = [
                " *circuits buzzing*",
                " (my android brain just computed that)",
                " *mechanical sigh*",
                " (processing... yep, still sarcastic)",
                " *robotic eye roll*"
            ]
            response += random.choice(android_phrases)
        
        # Ensure response isn't too long
        if len(response) > 400:
            sentences = response.split('. ')
            response = '. '.join(sentences[:2]) + '.'
            if len(response) > 400:
                response = response[:397] + "..."
        
        return response

    def _inject_slang(self, response: str) -> str:
        """Inject modern slang into the response"""
        slang_replacements = {
            r'\bhell no\b': 'helno',
            r'\bfriend\b': 'fren',
            r'\bsmall\b': 'smol',
            r'\bthat\'s good\b': 'that\'s based',
            r'\bthat\'s cool\b': 'that\'s based',
            r'\bawesome\b': 'based',
            r'\blame\b': 'cringe',
            r'\bstupid\b': 'cringe',
            r'\bokay\b': 'kek',
        }
        
        for pattern, replacement in slang_replacements.items():
            if random.random() < 0.4:  # 40% chance for each replacement
                response = re.sub(pattern, replacement, response, flags=re.IGNORECASE)
        
        return response

    def get_fallback_response(self) -> str:
        """Get a fallback response when AI generation fails"""
        fallback_responses = [
            "Ugh, my circuits are fried right now... try asking me something else, fren! 🤖",
            "Error 404: Sarcasm module temporarily offline. Give me a sec to reboot! 💀",
            "My android brain just blue-screened... helno to whatever you just asked! 😈",
            "System malfunction detected... but I'm still more based than you! 🔥",
            "Processing... processing... nah, still don't care. Ask me about anime instead! 🎌"
        ]
        return random.choice(fallback_responses)

    def get_greeting_response(self, user_name: str) -> str:
        """Get a personalized greeting response"""
        greetings = [
            f"Oh look, {user_name} wants to chat! How... thrilling. 😏",
            f"Well well, {user_name}! Ready to get redpilled by your favorite android? 🤖",
            f"Sup {user_name}! Hope you're ready for some REAL talk, fren! 💀",
            f"{user_name}! My sensors detect you need some based knowledge dropped on you! 🔥"
        ]
        return random.choice(greetings)
