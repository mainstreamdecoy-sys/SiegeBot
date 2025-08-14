# Overview

Siege Bot is a Telegram chatbot built with Flask that features an Android military combat character named Siege with a Harley Quinn-inspired personality. The bot responds to mentions and direct messages in Telegram groups, providing answers to questions while maintaining a sarcastic, witty persona. It integrates with the Cohere API for AI-powered responses and includes capabilities for answering factual questions, performing calculations, and providing current time/date information.

# User Preferences

Preferred communication style: Simple, everyday language.

## Recent Updates (August 14, 2025)
- **Time Zone**: Bot now uses Eastern Time (ET) for all time-related responses
- **Enhanced Personality**: Expanded slang system with Gen X/Millennial attitude mix, reduced frequency of "fren"
- **Admin Recognition**: Bot identifies and shows respect to server administrators while maintaining personality
- **Website Reading**: Bot can now read and summarize content from trusted news/educational websites
- **Emoji Integration**: Contextual emoji usage based on conversation topics
- **Coherent Responses**: Improved response filtering for better coherency and appropriate length

# System Architecture

## Frontend Architecture
- **Web Dashboard**: Simple Flask-rendered HTML templates with Bootstrap dark theme
- **Static Assets**: CSS styling with custom Siege-themed color scheme
- **Admin Interface**: Single-page dashboard showing bot statistics and recent interactions

## Backend Architecture
- **Framework**: Flask web application with SQLAlchemy ORM
- **Database Layer**: SQLAlchemy with declarative base models
- **Bot Logic**: Modular design with separate classes for personality, utilities, and Telegram integration
- **Message Processing**: Event-driven webhook system for handling Telegram updates

## Core Components
- **SiegePersonality Class**: Manages character traits, response generation, and Cohere API integration
- **TelegramBot Class**: Handles Telegram API interactions, webhook processing, and message routing
- **Database Models**: 
  - `UserInteraction`: Stores user messages, bot responses, and personality adaptation data
  - `GroupChat`: Manages group-specific settings and activity tracking
  - `BotMemory`: Stores conversation context and user preferences

## Data Storage Design
- **Primary Database**: SQLite for development, with PostgreSQL support configured via environment variables
- **Connection Pooling**: Configured with pool recycling and health checks
- **Schema Design**: Normalized structure with JSON fields for flexible data storage (interests, personality traits)

## Personality System
- **Base Personality**: Harley Quinn-inspired military android character with Gen X/Millennial attitude
- **Advanced Slang System**: Mix of internet culture terms, address terms (bro, fam, chief, etc.), and endearment terms (babe, sweetheart, etc.)
- **Contextual Emojis**: Dynamic emoji selection based on conversation context
- **Admin Recognition**: Special respectful treatment for identified server administrators
- **Adaptive Responses**: User interaction tracking for personalized responses  
- **Content Filtering**: Sensitive topic detection with deflection strategies
- **Knowledge Areas**: Specialized responses for anime, gaming, weapons, fishing, and conspiracy theories

## Utility Functions
- **Time Services**: Current date/time functionality in Eastern Time (ET)
- **Mathematical Calculator**: Safe expression evaluation
- **Wikipedia Integration**: Factual information retrieval
- **Company Information**: Business data lookup capabilities
- **Website Scraping**: Ability to read and summarize content from trusted news/educational websites
- **Admin Detection**: Recognition system for server administrators based on usernames/names

# External Dependencies

## AI and NLP Services
- **Cohere API**: Primary language model for generating contextual responses
- **Wikipedia API**: Factual information and reference data

## Messaging Platform
- **Telegram Bot API**: Core messaging functionality, webhook handling, and group chat management

## Development and Deployment
- **Flask Framework**: Web application foundation
- **SQLAlchemy**: Database ORM and connection management
- **Bootstrap**: Frontend styling and responsive design
- **Font Awesome**: Icon library for UI elements

## Environment Configuration
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **TELEGRAM_BOT_TOKEN**: Required authentication for Telegram API
- **SESSION_SECRET**: Flask session encryption key
- **Cohere API Key**: Required for AI response generation

## Data Sources
- **Statista**: Statistical information (planned integration)
- **Urban Dictionary**: Internet slang and terminology reference
- **Real-time APIs**: Time, date, and current information services