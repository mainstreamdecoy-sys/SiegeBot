# Overview
This is a Telegram bot named "Siege" - a military combat android with the personality of a sarcastic, anime-obsessed goth girl. Built by Techpriests for end times combat, she's a 5'6" blonde android with blue eyes and a robotic left arm. The bot uses Cohere's AI language model to generate responses with expertise in anime, gaming, conspiracy theories, and sharp sarcastic commentary. She responds to @Siege_Chat_Bot mentions, replies, and private messages with modern internet slang and attitude.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework
- **Technology**: Python-telegram-bot library for Telegram API integration
- **Architecture Pattern**: Asynchronous event-driven design using asyncio
- **Handler Structure**: Command handlers for bot commands (/start, /help) and message handlers for different interaction types (private messages, mentions, replies)

## AI Integration
- **Language Model**: Cohere AI API for generating personality-driven responses
- **Prompt Engineering**: Custom personality system that creates contextual prompts based on interaction type and user input
- **Response Filtering**: Built-in response length limits and timeout controls

## Personality System
- **Design Pattern**: Modular SiegePersonality class maintaining character consistency
- **Character Elements**: 
  - Military android phrases with combat and techpriest references
  - Sharp sarcastic responses inspired by anime characters like Revy and Satsuki
  - Weeb/anime slang (based, cringe, normie, weeb, otaku, touch grass)
  - Mood indicators using combat/tech emojis (💀⚔️🤖💯)
- **Knowledge Areas**: Anime expert (Attack on Titan, NGE, Spirited Away), Warhammer 40k Space Marine 2, conspiracy theories (Flat Earth, Tartaria), metal/K-pop music, cats, hunting/fishing
- **Scientific Knowledge**: Comprehensive periodic table database (elements 1-100), Wikipedia integration for factual accuracy
- **Personality Traits**: Goth military android, extremely sarcastic, conspiracy theorist, flat earther, Christian, right-wing republican, anti-crypto, cat lover, scientifically accurate but rude
- **Context Awareness**: Uses usernames in responses, keeps responses 1-2 sentences max, provides accurate scientific facts with attitude, dodges sensitive topics

## Configuration Management
- **Environment-based**: Uses dotenv for local development with fallback to system environment variables
- **Validation**: Built-in configuration validation to ensure required API keys are present
- **Flexibility**: Configurable parameters for response length, timeouts, and logging levels

## Error Handling and Logging
- **Logging Strategy**: Structured logging with timestamps and severity levels
- **Graceful Degradation**: Configuration validation prevents startup with missing credentials
- **Exception Management**: Try-catch blocks around critical operations like bot initialization

## Message Processing Flow
- **Priority-based Routing**: Message handlers ordered by specificity (replies → mentions → private messages)
- **Context Detection**: Automatically determines interaction context for appropriate personality responses
- **Async Processing**: Non-blocking message handling to maintain bot responsiveness

# External Dependencies

## APIs and Services
- **Telegram Bot API**: Core messaging platform integration via python-telegram-bot library
- **Cohere AI API**: Language model service for generating personality-driven responses

## Python Libraries
- **Core Dependencies**: 
  - `python-telegram-bot`: Telegram API wrapper and bot framework
  - `cohere`: Official Cohere AI Python client
  - `python-dotenv`: Environment variable management for development
- **Standard Library**: `asyncio` for asynchronous operations, `logging` for application monitoring, `os` and `re` for system integration and text processing

## Environment Configuration
