# Overview

This is Siege, a sarcastic anime android Telegram chatbot with Harley Quinn personality powered by Cohere AI. Siege responds to @Siege_Chat_Bot mentions and replies with witty, sarcastic responses while having deep knowledge of anime, gaming, conspiracy theories, weapons, fishing, and more. The bot uses direct Telegram Bot API integration (bypassing python-telegram-bot library issues) and Cohere's API to generate AI-powered responses with a complex, multi-faceted personality.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Application Structure
The application follows a modular architecture with clear separation of concerns:

- **bot.py** - Contains the main `SiegeChatBot` class that handles all bot logic and message processing
- **config.py** - Centralized configuration management using environment variables with validation
- **main.py** - Entry point that initializes and runs the bot with proper signal handling

## Bot Architecture
The chatbot uses an event-driven architecture built on the python-telegram-bot framework:

- **Handler-based Processing** - Uses CommandHandler for commands (/start, /help) and MessageHandler for mentions and replies
- **Asynchronous Operations** - Built with async/await pattern for non-blocking message processing
- **Error Handling** - Implements retry logic and graceful error handling for network issues
- **Signal Management** - Proper shutdown handling for graceful termination

## Configuration Management
Environment-based configuration system with validation:

- **Environment Variables** - All sensitive data (API keys, tokens) stored in environment variables
- **Validation Layer** - Configuration validation ensures required settings are present before startup
- **Flexible Settings** - Configurable timeouts, message limits, and logging levels

## Message Processing Flow
1. Bot receives Telegram messages through webhook or polling
2. Filters messages for mentions or replies to the bot
3. Sends message content to Cohere AI API for response generation
4. Returns AI-generated response back to the Telegram chat
5. Implements timeout and length limits for responses

# External Dependencies

## AI Service Integration
- **Cohere AI API** - Primary AI service for generating conversational responses using the "command-r-plus" model
- **API Key Authentication** - Requires Cohere API key for service access

## Telegram Bot Platform
- **Telegram Bot API** - Core platform integration using python-telegram-bot library
- **Bot Token Authentication** - Requires Telegram Bot Token from BotFather
- **Webhook/Polling Support** - Supports both webhook and polling modes for receiving messages

## Python Libraries
- **python-telegram-bot** - Official Telegram Bot API wrapper
- **cohere** - Official Cohere AI Python SDK
- **python-dotenv** - Environment variable management
- **asyncio** - Asynchronous programming support

## Environment Configuration
- **.env file support** - Local development environment variable management
- **System environment variables** - Production deployment configuration support