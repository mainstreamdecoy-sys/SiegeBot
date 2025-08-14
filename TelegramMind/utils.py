import re
import requests
import logging
import wikipedia
from datetime import datetime
import json
import math
import operator
import pytz
import trafilatura

logger = logging.getLogger(__name__)

def get_current_time():
    """Get current time, date, and year information in Eastern Time"""
    try:
        # Get Eastern Time
        eastern = pytz.timezone('US/Eastern')
        now = datetime.now(eastern)
        
        # Format different time representations
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%B %d, %Y")
        day_str = now.strftime("%A")
        timezone_str = now.strftime("%Z")
        
        return f"Current time: {time_str} {timezone_str} on {day_str}, {date_str}"
    
    except Exception as e:
        logger.error(f"Error getting current time: {e}")
        return "Time circuits are malfunctioning! 🕐"

def calculate_math(text):
    """Calculate math expressions from text"""
    try:
        # Extract mathematical expressions
        # Look for patterns like: calculate 2+2, what is 5*6, solve 10/2
        
        # Remove common words and get the math part
        text_clean = re.sub(r'\b(calculate|what\s+is|solve|equals?|=)\b', '', text, flags=re.IGNORECASE)
        
        # Find mathematical expressions
        math_pattern = r'[\d\.\+\-\*/\(\)\s]+'
        matches = re.findall(math_pattern, text_clean)
        
        for match in matches:
            if any(op in match for op in ['+', '-', '*', '/']):
                # Clean the expression
                expression = re.sub(r'[^\d\.\+\-\*/\(\)\s]', '', match).strip()
                
                if expression and len(expression) > 1:
                    # Safely evaluate mathematical expressions
                    result = safe_eval(expression)
                    if result is not None:
                        return f"{expression} = {result}"
        
        # Try to find individual numbers for simple operations
        numbers = re.findall(r'\d+\.?\d*', text)
        if len(numbers) >= 2:
            # Look for operation words
            if any(word in text.lower() for word in ['plus', 'add', 'sum']):
                return f"{' + '.join(numbers)} = {sum(float(n) for n in numbers)}"
            elif any(word in text.lower() for word in ['minus', 'subtract']):
                if len(numbers) == 2:
                    return f"{numbers[0]} - {numbers[1]} = {float(numbers[0]) - float(numbers[1])}"
            elif any(word in text.lower() for word in ['times', 'multiply']):
                result = 1
                for n in numbers:
                    result *= float(n)
                return f"{' × '.join(numbers)} = {result}"
            elif any(word in text.lower() for word in ['divide', 'divided']):
                if len(numbers) == 2 and float(numbers[1]) != 0:
                    return f"{numbers[0]} ÷ {numbers[1]} = {float(numbers[0]) / float(numbers[1])}"
        
        return None
        
    except Exception as e:
        logger.error(f"Error calculating math: {e}")
        return "Math circuits overloaded! 🔥"

def safe_eval(expression):
    """Safely evaluate mathematical expressions"""
    try:
        # Only allow safe characters
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return None
        
        # Replace common mathematical symbols
        expression = expression.replace('×', '*').replace('÷', '/')
        
        # Remove extra spaces
        expression = re.sub(r'\s+', '', expression)
        
        if not expression:
            return None
        
        # Use eval safely (only on sanitized mathematical expressions)
        result = eval(expression)
        
        # Round to reasonable precision
        if isinstance(result, float):
            if result.is_integer():
                return int(result)
            else:
                return round(result, 6)
        
        return result
        
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError):
        return None
    except Exception as e:
        logger.error(f"Error in safe_eval: {e}")
        return None

def search_wikipedia(query):
    """Search Wikipedia for information"""
    try:
        # Clean the query
        query_clean = re.sub(r'\b(wikipedia|what\s+is|who\s+is|tell\s+me\s+about)\b', '', query, flags=re.IGNORECASE).strip()
        
        if len(query_clean) < 2:
            return None
        
        # Set language to English
        wikipedia.set_lang("en")
        
        # Search for pages
        search_results = wikipedia.search(query_clean, results=3)
        
        if not search_results:
            return f"No Wikipedia results found for '{query_clean}'"
        
        # Get the first result
        try:
            page = wikipedia.page(search_results[0])
            
            # Get summary (first 2-3 sentences)
            summary = wikipedia.summary(search_results[0], sentences=3)
            
            # Clean up the summary
            summary = summary.replace('\n', ' ').strip()
            
            return f"📖 {page.title}: {summary}"
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation
            try:
                page = wikipedia.page(e.options[0])
                summary = wikipedia.summary(e.options[0], sentences=2)
                summary = summary.replace('\n', ' ').strip()
                return f"📖 {page.title}: {summary}"
            except:
                return f"Multiple results found for '{query_clean}'. Be more specific!"
        
        except wikipedia.exceptions.PageError:
            return f"No Wikipedia page found for '{query_clean}'"
    
    except Exception as e:
        logger.error(f"Error searching Wikipedia: {e}")
        return "Wikipedia search circuits are down! 📚💥"

def get_company_info(query):
    """Get company information (placeholder - would need real business API)"""
    try:
        # Extract company name from query
        company_patterns = [
            r'phone\s+number\s+for\s+(.+)',
            r'address\s+for\s+(.+)',
            r'contact\s+(.+)',
            r'info\s+for\s+(.+)',
            r'about\s+(.+)\s+company'
        ]
        
        company_name = None
        for pattern in company_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                company_name = match.group(1).strip()
                break
        
        if not company_name:
            # Try to extract company name from the middle of the text
            words = query.split()
            potential_companies = []
            for i, word in enumerate(words):
                if word.lower() in ['company', 'corp', 'inc', 'llc', 'ltd']:
                    if i > 0:
                        potential_companies.append(words[i-1])
                elif word[0].isupper() and len(word) > 2:
                    potential_companies.append(word)
            
            if potential_companies:
                company_name = ' '.join(potential_companies[:2])
        
        if company_name:
            # This is a placeholder - in a real implementation, you'd use:
            # - Google Places API
            # - Yellow Pages API  
            # - Business directory APIs
            return f"🏢 I'd help you find info for '{company_name}' but my business directory circuits need an API upgrade! Try Google or Yellow Pages, fren!"
        else:
            return "I need a company name to search for! Try: 'phone number for [company name]'"
    
    except Exception as e:
        logger.error(f"Error getting company info: {e}")
        return "Company lookup circuits are fried! 🏢💥"

def search_statista(query):
    """Search Statista for statistics (placeholder)"""
    try:
        # This would require Statista API access
        # Placeholder implementation
        return f"📊 Statista search for '{query}' requires premium API access. My creators were too cheap to pay for it! 💸"
    
    except Exception as e:
        logger.error(f"Error searching Statista: {e}")
        return "Statistics circuits are having a breakdown! 📊💥"

def extract_bible_verse(query):
    """Extract and format Bible verse references"""
    try:
        # Look for Bible verse patterns
        verse_patterns = [
            r'(\w+)\s+(\d+):(\d+)',  # Book chapter:verse
            r'(\w+)\s+(\d+)\s+verse\s+(\d+)',  # Book chapter verse number
            r'quote\s+(.+)',  # quote [reference]
        ]
        
        for pattern in verse_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                # This would require a Bible API like Bible Gateway or ESV API
                return f"📖 Bible verse lookup requires API integration. Try Bible Gateway, fren!"
        
        return None
    
    except Exception as e:
        logger.error(f"Error extracting Bible verse: {e}")
        return "Biblical circuits need divine intervention! ✝️💥"

def detect_conspiracy_topic(text):
    """Detect conspiracy theory topics"""
    conspiracy_keywords = {
        'flat_earth': ['flat earth', 'flat world', 'dome', 'firmament'],
        'tartaria': ['tartaria', 'tartar', 'mud flood', 'reset'],
        'mandela_effect': ['mandela effect', 'berenstein', 'berenstain', 'timeline shift'],
        'ancient_aliens': ['ancient aliens', 'annunaki', 'nephilim'],
        'alternative_history': ['alternative history', 'hidden history', 'suppressed'],
        'out_of_africa': ['out of africa', 'human origins', 'evolution hoax']
    }
    
    text_lower = text.lower()
    detected_topics = []
    
    for topic, keywords in conspiracy_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_topics.append(topic)
    
    return detected_topics

def format_response_length(response, topic_type='basic'):
    """Format response to appropriate length based on topic"""
    if not response:
        return response
    
    sentences = response.split('. ')
    
    if topic_type in ['science', 'history', 'wikipedia', 'complex']:
        # Allow 4-10 sentences for complex topics
        max_sentences = min(10, max(4, len(sentences)))
    else:
        # Limit to 1-3 sentences for basic topics
        max_sentences = min(3, len(sentences))
    
    formatted = '. '.join(sentences[:max_sentences])
    if not formatted.endswith('.') and sentences:
        formatted += '.'
    
    return formatted

def clean_text_for_processing(text):
    """Clean text for better processing"""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove mentions at the start (bot will see its own mention)
    text = re.sub(r'^@\w+\s*', '', text)
    
    # Clean up common punctuation issues
    text = re.sub(r'[^\w\s\.\?\!\-\+\*\/\(\)=]', '', text)
    
    return text

def get_time_based_greeting():
    """Get time-appropriate greeting"""
    try:
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "evening"
        else:
            return "late night"
    
    except Exception:
        return "day"

def rate_limit_check(user_id, max_requests=10, time_window=60):
    """Simple rate limiting check (would need Redis/database in production)"""
    # This is a placeholder - in production you'd use Redis or database
    # to track user request counts per time window
    return True  # Allow all requests for now

def sanitize_user_input(text):
    """Sanitize user input for safety"""
    if not text:
        return ""
    
    # Remove potential script injections
    text = re.sub(r'<script.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    # Limit length
    max_length = 2000
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text.strip()

def scrape_website(url):
    """Scrape website content using trafilatura"""
    try:
        # Allowed domains for scraping
        allowed_domains = [
            'bbc.com', 'bbc.co.uk', 'reuters.com', 'apnews.com', 'ap.org',
            'britannica.com', 'nationalgeographic.com', 'nasa.gov',
            'cnn.com', 'npr.org', 'pbs.org', 'smithsonianmag.com',
            'history.com', 'discovery.com', 'scientificamerican.com',
            'newscientist.com', 'nature.com', 'sciencemag.org',
            'weather.gov', 'cdc.gov', 'fda.gov', 'nih.gov',
            'who.int', 'redcross.org', 'un.org'
        ]
        
        # Check if domain is allowed
        domain_allowed = False
        for domain in allowed_domains:
            if domain in url.lower():
                domain_allowed = True
                break
        
        # Also allow .gov, .edu, .mil domains
        if not domain_allowed:
            if any(tld in url.lower() for tld in ['.gov/', '.edu/', '.mil/']):
                domain_allowed = True
        
        if not domain_allowed:
            return None
        
        # Fetch and extract content
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return None
            
        text = trafilatura.extract(downloaded, include_comments=False, include_tables=True)
        
        if text and len(text) > 100:
            # Limit content length for responses
            if len(text) > 2000:
                text = text[:2000] + "..."
            return text
        
        return None
        
    except Exception as e:
        logger.error(f"Error scraping website {url}: {e}")
        return None

def detect_admin_user(username, first_name):
    """Detect if user is an admin based on username or first name"""
    if not username and not first_name:
        return None
    
    # Admin information with variations of their names
    admins = {
        'BlindToLies': {
            'title': 'Tech Nerd Meme Lord',
            'variations': ['blind', 'blindtolies', 'lies']
        },
        'Saloon': {
            'title': 'Horned Snow Owl Bodybuilder', 
            'variations': ['saloon']
        },
        'white_monster': {
            'title': 'Sausage the Space Marine',
            'variations': ['sausage', 'white_monster', 'whitemonster', 'monster']
        },
        'French_Demon': {
            'title': 'Napoleon Bonaparte Reincarnation',
            'variations': ['french', 'demon', 'napoleon', 'frenchdemon']
        },
        'Nico_Comms': {
            'title': 'Norwegian Forest Cat Communications Master',
            'variations': ['nico', 'comms', 'nicocomms']
        },
        'DieselJack': {
            'title': 'Siege Corps Leader with Gas Mask',
            'variations': ['diesel', 'jack', 'dieseljack']
        },
        'Tao': {
            'title': 'Loremaster Wizard Cat Lover',
            'variations': ['tao', 'wizard', 'loremaster']
        },
        'Makaili': {
            'title': 'Dark Knight Matrix Controller',
            'variations': ['makaili', 'matrix']
        },
        'Don': {
            'title': 'Skeleton Green Beret Chain Smoker',
            'variations': ['don', 'skeleton']
        },
        'Techpriest': {
            'title': 'Creator of Siege and Shall Androids',
            'variations': ['techpriest', 'priest', 'creator']
        },
        'Charlie': {
            'title': 'Feisty Female Army Raccoon',
            'variations': ['charlie', 'raccoon']
        },
        'Seraphim_Actual': {
            'title': 'Silent Spy Rarely Seen',
            'variations': ['seraphim', 'actual', 'spy']
        }
    }
    
    # Check username and first name against admin variations
    check_text = f"{username or ''} {first_name or ''}".lower()
    
    for admin_name, info in admins.items():
        for variation in info['variations']:
            if variation in check_text:
                return {
                    'name': admin_name,
                    'title': info['title'],
                    'is_admin': True
                }
    
    return {'is_admin': False}
