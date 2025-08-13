import TelegramBot from 'node-telegram-bot-api';
import { generateConversationalResponse, shouldRespondToMessage } from './openai.js';
import { storage } from '../storage.js';

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN || process.env.BOT_TOKEN || "your-telegram-bot-token";

class SobertBot {
  private bot: TelegramBot;
  private isRunning: boolean = false;

  constructor() {
    if (!TELEGRAM_BOT_TOKEN || TELEGRAM_BOT_TOKEN === "your-telegram-bot-token" || TELEGRAM_BOT_TOKEN.length < 40) {
      console.error('Invalid Telegram bot token. Please check your TELEGRAM_BOT_TOKEN environment variable.');
      console.error('Token format should be: 123456789:ABCdefGHIjklMNOpqrSTUvwxYZ-1234567890');
      console.error('Current token length:', TELEGRAM_BOT_TOKEN.length);
    }
    
    this.bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { 
      polling: false,
      request: {
        agentOptions: {
          keepAlive: true,
          family: 4
        }
      }
    });
    this.setupCommands();
    this.setupMessageHandlers();
  }

  public async start() {
    if (!this.isRunning) {
      try {
        // Test the bot token first
        const botInfo = await this.bot.getMe();
        console.log('Bot info:', JSON.stringify(botInfo, null, 2));
        
        await this.bot.startPolling();
        this.isRunning = true;
        console.log('Siege Chat Bot started successfully');
        console.log('Bot username:', botInfo.username);
      } catch (error) {
        console.error('Failed to start Telegram bot:', error.message);
        console.error('Please check your TELEGRAM_BOT_TOKEN');
        this.isRunning = false;
      }
    }
  }

  public stop() {
    if (this.isRunning) {
      this.bot.stopPolling();
      this.isRunning = false;
      console.log('Siege Chat Bot stopped');
    }
  }

  public getStatus() {
    return {
      isRunning: this.isRunning,
      botUsername: '@Siege_Chat_Bot'
    };
  }

  private setupCommands() {
    // Help command
    this.bot.onText(/\/help/, async (msg) => {
      const chatId = msg.chat.id;
      const helpText = `
🤖 *Siege Chat Bot Commands*

/help - Display this help message
/stats - Show bot statistics and usage data
/option_set reply_prob <0-1.0> - Adjust reply probability (admin only)
/option_set sticker_prob <0-1.0> - Control sticker frequency (admin only)

I'm your crazy AI chatbot buddy! Let's have some fun, puddin'! 💥🎭
      `;
      
      await this.bot.sendMessage(chatId, helpText, { parse_mode: 'Markdown' });
      await this.logActivity('command', 'Help command used', `Chat ${chatId}`);
    });

    // Stats command
    this.bot.onText(/\/stats/, async (msg) => {
      const chatId = msg.chat.id;
      try {
        const stats = await storage.getBotStats();
        const config = await storage.getBotConfig();
        
        const statsText = `
📊 *Bot Statistics*

💬 Total Messages: ${stats.totalMessages.toLocaleString()}
👥 Active Groups: ${stats.activeGroups}
⚡ Response Rate: ${(stats.responseRate * 100).toFixed(1)}%
🎯 Reply Probability: ${(config.replyProbability * 100).toFixed(0)}%
🎭 Sticker Probability: ${(config.stickerProbability * 100).toFixed(0)}%

🧠 AI Model: Cohere Command-R
📚 AI Provider: Cohere
        `;
        
        await this.bot.sendMessage(chatId, statsText, { parse_mode: 'Markdown' });
        await this.logActivity('command', 'Stats command used', `Chat ${chatId}`);
      } catch (error) {
        await this.bot.sendMessage(chatId, 'Error retrieving statistics. Please try again later.');
      }
    });

    // Option set command (admin only for now)
    this.bot.onText(/\/option_set (\w+) ([\d.]+)/, async (msg, match) => {
      const chatId = msg.chat.id;
      
      if (!match || match.length < 3) {
        await this.bot.sendMessage(chatId, 'Usage: /option_set <option> <value>\nOptions: reply_prob, sticker_prob');
        return;
      }

      const option = match[1];
      const value = parseFloat(match[2]);

      if (isNaN(value) || value < 0 || value > 1) {
        await this.bot.sendMessage(chatId, 'Value must be a number between 0 and 1');
        return;
      }

      try {
        const config = await storage.getBotConfig();
        
        if (option === 'reply_prob') {
          await storage.updateBotConfig({ replyProbability: value });
          await this.bot.sendMessage(chatId, `✅ Reply probability set to ${(value * 100).toFixed(0)}%`);
        } else if (option === 'sticker_prob') {
          await storage.updateBotConfig({ stickerProbability: value });
          await this.bot.sendMessage(chatId, `✅ Sticker probability set to ${(value * 100).toFixed(0)}%`);
        } else {
          await this.bot.sendMessage(chatId, 'Unknown option. Available: reply_prob, sticker_prob');
          return;
        }

        await this.logActivity('config', `${option} updated to ${value}`, `Chat ${chatId}`);
      } catch (error) {
        await this.bot.sendMessage(chatId, 'Error updating configuration. Please try again later.');
      }
    });
  }

  private setupMessageHandlers() {
    this.bot.on('message', async (msg) => {
      // Skip if it's a command
      if (msg.text?.startsWith('/')) {
        return;
      }

      const chatId = msg.chat.id;
      const messageText = msg.text || '';
      const isGroup = msg.chat.type === 'group' || msg.chat.type === 'supergroup';
      const isPrivate = msg.chat.type === 'private';

      try {
        // Update message count
        await storage.incrementMessageCount();

        // Get current configuration
        const config = await storage.getBotConfig();

        // Determine if we should respond
        let shouldRespond = false;

        if (isPrivate) {
          // In private chats, use regular probability
          shouldRespond = await shouldRespondToMessage(messageText, config.replyProbability);
        } else if (isGroup) {
          // In groups, check configuration and mentions
          if (!config.groupAutoRespond) {
            return;
          }

          const isMentioned = msg.reply_to_message?.from?.username === 'siege_chat_bot' ||
                            messageText.toLowerCase().includes('siege') ||
                            messageText.includes('@siege_chat_bot');

          if (config.mentionsOnly) {
            shouldRespond = isMentioned;
          } else {
            shouldRespond = isMentioned || await shouldRespondToMessage(messageText, config.replyProbability * 0.5); // Lower probability in groups
          }
        }

        if (!shouldRespond) {
          return;
        }

        // Generate AI response
        const context = isGroup ? `Group chat: ${msg.chat.title || 'Unknown'}` : 'Private chat';
        const response = await generateConversationalResponse(messageText, context);

        // Send response
        await this.bot.sendMessage(chatId, response, {
          reply_to_message_id: msg.message_id
        });

        // Log activity
        const activitySource = isGroup ? msg.chat.title || 'Group Chat' : 'Private Chat';
        await this.logActivity('response', 'AI response sent', activitySource);

        // Update response rate
        await storage.updateResponseRate();

      } catch (error) {
        console.error('Error handling message:', error);
        
        // Send error message only in private chats to avoid spam
        if (isPrivate) {
          await this.bot.sendMessage(chatId, "I'm having trouble right now. Please try again in a moment! 🤖");
        }
      }
    });

    // Handle new group joins
    this.bot.on('new_chat_members', async (msg) => {
      const newMembers = msg.new_chat_members || [];
      const botJoined = newMembers.some(member => member.username === 'SobertBot' || member.is_bot);

      if (botJoined) {
        const chatId = msg.chat.id;
        const welcomeMessage = `
🐺 Hello! I'm SobertBot, an AI chatbot.

I can engage in conversations and respond to messages. Use /help to see available commands.

I'll participate respectfully in your group discussions. You can configure my behavior using the /option_set commands.
        `;

        await this.bot.sendMessage(chatId, welcomeMessage);
        await storage.incrementGroupCount();
        await this.logActivity('group', 'Added to new group', msg.chat.title || 'Unknown Group');
      }
    });
  }

  private async logActivity(type: string, description: string, source?: string) {
    try {
      await storage.addRecentActivity({
        type,
        description,
        source: source || undefined
      });
    } catch (error) {
      console.error('Error logging activity:', error);
    }
  }
}

export const sobertBot = new SobertBot();
