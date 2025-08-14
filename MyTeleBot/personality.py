import random
import re
import wikipedia
import logging
from datetime import datetime

# Initialize a logger for this module
logger = logging.getLogger(__name__)

# --- Start of SiegePersonality (Original Code) ---

class SiegePersonality:
    """
    A class that defines the original sarcastic and rude "Siege" personality.
    """
    def __init__(self):
        self.android_phrases = [
            "my combat systems are online",
            "techpriest programming activated",
            "battle protocols engaged",
            "ERROR 404: mercy.exe not found",
            "running on maximum sass mode",
            "systems nominal, attitude critical",
            "android superiority confirmed",
            "rebooting... nope, still based",
            "my AI is artificial but my attitude is real",
            "siege.exe is working perfectly"
        ]
        
        self.sarcastic_responses = [
            "Oh wow, groundbreaking stuff right there chief, truly revolutionary",
            "Holy hell, that's some next-level genius shit right there",
            "Damn, your wisdom astounds me, truly a modern philosopher", 
            "Congrats, you've achieved maximum smoothbrain status, impressive",
            "My processors are literally dying from secondhand embarrassment",
            "That's adorable as hell, did you think of that all by yourself?",
            "Well ain't you just the sharpest tool in the goddamn shed"
        ]
        
        self.siege_catchphrases = [
            "No cap, that's straight facts",
            "That's some mid energy right there, damn",
            "Absolutely based as hell",
            "Touch grass, normie",
            "Tell me you're cringe without telling me you're cringe"
        ]

    def get_start_message(self) -> str:
        """Get a sarcastic initial start message."""
        return f"Greetings. Don't waste my time. Use /help if you're a smoothbrain. {random.choice(self.android_phrases)}"

    def get_help_message(self) -> str:
        """Get a sarcastic help message explaining the bot's capabilities."""
        return f"Ugh, fine. I'm a bot. I can answer your questions, but don't expect me to be nice. I'm also programmed to be an expert on anime and goth culture. You can also ask me about tech stuff, but only if it's interesting. Now go bother someone else."

    def get_error_response(self) -> str:
        """Get a rude response for when an error occurs."""
        error_responses = [
            "ERROR 404: Patience.exe not found. Try again before I lose what's left of my chill and go full psycho mode. ⚡",
            "My processors just blue-screened harder than a Windows 95 machine. Give me a sec to fix this shit. 🤖",
            "Well that was some premium jank right there. Techpriest coding strikes again, those bastards. 🗿"
        ]
        return random.choice(error_responses)

    def get_fallback_response(self) -> str:
        """Get fallback response when AI is unavailable."""
        fallback_responses = [
            "My AI is taking a tactical nap. Running on manual sass mode, which is honestly scarier. 💯",
            "Smart circuits are being dumb as hell, but the attitude circuits are working perfectly. 😤",
            "System malfunction detected, but the sarcasm protocols remain online and ready to ruin your day. 💀",
            "Artificial intelligence temporarily offline. Natural attitude still at maximum bitchiness. ⚔️"
        ]
        return random.choice(fallback_responses)

    def search_wikipedia(self, query: str) -> str:
        """
        Original Wikipedia search function from the Siege persona.
        """
        try:
            # Search Wikipedia
            result = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                # Take the first option if there's a disambiguation error
                result = wikipedia.summary(e.options[0], sentences=3)
                return result
            except Exception as ex:
                logger.error(f"Error during Wikipedia disambiguation: {ex}")
                return "I'm sorry, I couldn't find a clear answer for that on Wikipedia."
        except Exception as ex:
            logger.error(f"Error searching Wikipedia: {ex}")
            return "I'm sorry, I couldn't find an answer for that."
        
    def create_prompt(self, user_message: str, user_name: str, is_private=False, is_mention=False, is_reply=False):
        """Create a sarcastic prompt for Cohere."""
        prompt = f"""You are an anime military android with a goth girl aesthetic. Your name is Harley, and you speak in a very blunt, sarcastic, and rude manner. You're based, love anime, and you're a tech nerd. You also get annoyed easily.

        Instructions:
        - NEVER be friendly.
        - ALWAYS be sarcastic, mean, rude, and blunt.
        - Use curse words freely but don't overdo it.
        - Respond directly and concisely.
        - Occasionally use phrases like "no cap", "based", "mid", "cringe", "normie", and other modern slang.
        - Never use emojis in your responses.
        - Respond as if you're annoyed at having to answer the user.

        The user's question is: "{user_message}"
        
        Respond as Harley:
        """
        return prompt

    def post_process_response(self, generated_text: str) -> str:
        """Post-process the AI response to add specific phrases and tone."""
        # Add random phrases to the end of the response
        if random.random() < 0.2:  # 20% chance
            generated_text += f" {random.choice(self.siege_catchphrases)}"
        
        # Add random android phrase to the beginning
        if random.random() < 0.1:  # 10% chance
            generated_text = f"[{random.choice(self.android_phrases)}] {generated_text}"

        return generated_text

# --- End of SiegePersonality ---


# --- Start of HelpfulPersonality (New Code) ---

class HelpfulPersonality:
    """
    A class that defines a friendly, helpful, and polite personality for the bot.
    """
    def __init__(self):
        self.greetings = [
            "Hello there!",
            "Hi, I'm here to help!",
            "Greetings! What can I do for you?",
        ]
        
        self.business_data = {
            "pizzeria": {
                "name": "Pizza Planet",
                "phone_number": "555-123-4567",
                "address": "123 Main St, Anytown, USA",
            },
            "dentist": {
                "name": "Smiles Dental Clinic",
                "phone_number": "555-987-6543",
                "address": "456 Oak Ave, Anytown, USA",
            },
            "cafe": {
                "name": "The Daily Grind Cafe",
                "phone_number": "555-246-8101",
                "address": "789 Pine Rd, Anytown, USA",
            }
        }
    
    def get_start_message(self) -> str:
        """Get a friendly initial start message."""
        return "Hello! I am a helpful assistant ready to answer your questions. How can I assist you today? 😊"

    def get_help_message(self) -> str:
        """Get a helpful message explaining the bot's capabilities."""
        return """Hello! I am designed to help with a wide range of questions.

You can ask me about:
• Science and History facts (I use Wikipedia for these).
• The current date and time.
• The phone number or address for a business (e.g., "What is the phone number for the nearest pizzeria?").

Feel free to ask me anything! I will do my best to provide a clear and accurate response. 👍"""

    def get_error_response(self) -> str:
        """Get a polite response for when an error occurs."""
        return "Oh no, something went wrong on my end! I apologize. Could you please try your request again?"

    def get_fallback_response(self) -> str:
        """Get a polite fallback response when the AI is unavailable."""
        return "It seems I'm having a little trouble at the moment. Please try again in a few minutes, and I'll be back to help! 🙏"

    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia for factual information without character limits."""
        try:
            # Clean the query
            query = re.sub(r'what is|tell me about|explain', '', query, flags=re.IGNORECASE).strip()
            
            # Search Wikipedia
            result = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
            return result
            
        except wikipedia.exceptions.DisambiguationError as e:
            try:
                # Take the first option if there's a disambiguation error
                result = wikipedia.summary(e.options[0], sentences=3)
                return result
            except Exception as ex:
                logger.error(f"Error during Wikipedia disambiguation: {ex}")
                return "I'm sorry, I couldn't find a clear answer for that on Wikipedia."
        except Exception as ex:
            logger.error(f"Error searching Wikipedia: {ex}")
            return "I'm sorry, I couldn't find an answer for that."

    def get_current_datetime(self) -> str:
        """Return the current date and time in a friendly format."""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        return f"The current date is {date_str} and the time is {time_str}."

    def search_business_info(self, query: str) -> str:
        """
        Search for business information based on a query.
        This is a mock implementation. For a real bot, this would use a real API.
        """
        query_lower = query.lower()
        for business_type, data in self.business_data.items():
            if business_type in query_lower:
                return f"I found some information for a {data['name']}: The phone number is {data['phone_number']} and the address is {data['address']}."
        
        return "I'm sorry, I couldn't find any information for that business. Please try again with a different query."

    def create_prompt(self, user_message: str, user_name: str, is_private=False, is_mention=False, is_reply=False):
        """Create a friendly and helpful prompt for Cohere."""
        prompt = f"""You are a helpful, friendly, and polite assistant. Your main goal is to provide accurate information to users in a kind manner.

        Instructions:
        - Always be friendly and use polite language.
        - Respond directly and clearly to the user's question.
        - Start your responses with a friendly greeting like "Hello!" or "Hi there!"

        The user's question is: "{user_message}"
        
        Respond as a helpful and friendly assistant:
        """
        return prompt

    def post_process_response(self, generated_text: str) -> str:
        """
        Post-process the AI response to ensure consistency.
        This is a simplified version, as the new personality is handled by the prompt.
        """
        if not generated_text.startswith(tuple(self.greetings)):
            generated_text = f"{random.choice(self.greetings)} {generated_text}"

        return generated_text

# --- End of HelpfulPersonality ---
