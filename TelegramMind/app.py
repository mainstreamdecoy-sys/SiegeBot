import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///siege_bot.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Import after app creation to avoid circular imports
from telegram_bot import TelegramBot
from models import UserInteraction, GroupChat

# Initialize Telegram bot
bot = TelegramBot()

@app.route('/')
def index():
    """Admin dashboard for monitoring bot activity"""
    try:
        total_interactions = UserInteraction.query.count()
        recent_interactions = UserInteraction.query.order_by(UserInteraction.timestamp.desc()).limit(10).all()
        active_chats = GroupChat.query.filter_by(is_active=True).count()
        
        return render_template('index.html', 
                             total_interactions=total_interactions,
                             recent_interactions=recent_interactions,
                             active_chats=active_chats)
    except Exception as e:
        logger.error(f"Error loading dashboard: {e}")
        return render_template('index.html', 
                             total_interactions=0,
                             recent_interactions=[],
                             active_chats=0)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram bot"""
    try:
        update = request.get_json()
        logger.debug(f"Received update: {update}")
        
        if update:
            bot.process_update(update)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error", "message": "No update data"}), 400
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    """Set the webhook URL for the Telegram bot"""
    try:
        webhook_url = request.get_json().get('webhook_url') if request.get_json() else None
        if not webhook_url:
            return jsonify({"status": "error", "message": "webhook_url required"}), 400
            
        result = bot.set_webhook(webhook_url)
        return jsonify({"status": "ok", "result": result})
        
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/bot_info')
def bot_info():
    """Get bot information"""
    try:
        info = bot.get_bot_info()
        return jsonify({"status": "ok", "bot_info": info})
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Create tables
with app.app_context():
    try:
        db.create_all()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
