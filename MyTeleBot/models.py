from datetime import datetime
from app import db
import json

class UserInteraction(db.Model):
    """Store user interactions and personality adaptations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, nullable=False)
    username = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    chat_id = db.Column(db.BigInteger, nullable=False)
    message_text = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    message_type = db.Column(db.String(50))  # mention, reply, command, etc.
    
    # Personality adaptation fields
    user_attitude = db.Column(db.String(50))  # friendly, hostile, neutral, etc.
    interests = db.Column(db.Text)  # JSON string of detected interests
    interaction_count = db.Column(db.Integer, default=1)
    
    def __repr__(self):
        return f'<UserInteraction {self.user_id}: {self.message_text[:50]}...>'
    
    def get_interests_list(self):
        """Get interests as a list"""
        if self.interests:
            try:
                return json.loads(self.interests)
            except:
                return []
        return []
    
    def set_interests_list(self, interests_list):
        """Set interests from a list"""
        self.interests = json.dumps(interests_list)

class GroupChat(db.Model):
    """Store group chat information and settings"""
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    chat_title = db.Column(db.String(200))
    chat_type = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Group personality traits
    group_attitude = db.Column(db.String(50), default='neutral')
    dominant_interests = db.Column(db.Text)  # JSON string
    random_response_chance = db.Column(db.Float, default=0.1)  # 10% chance
    
    def __repr__(self):
        return f'<GroupChat {self.chat_id}: {self.chat_title}>'
    
    def get_dominant_interests(self):
        """Get dominant interests as a list"""
        if self.dominant_interests:
            try:
                return json.loads(self.dominant_interests)
            except:
                return []
        return []
    
    def set_dominant_interests(self, interests_list):
        """Set dominant interests from a list"""
        self.dominant_interests = json.dumps(interests_list)

class BotMemory(db.Model):
    """Store bot's memory and learning data"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BotMemory {self.key}: {self.value[:50]}...>'
