import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage.js";
import { sobertBot } from "./services/telegramBot.js";
import { insertBotConfigSchema } from "@shared/schema.js";

export async function registerRoutes(app: Express): Promise<Server> {
  // Bot management routes
  app.get("/api/bot/status", async (req, res) => {
    try {
      const status = sobertBot.getStatus();
      const stats = await storage.getBotStats();
      const config = await storage.getBotConfig();
      
      res.json({
        ...status,
        stats,
        config
      });
    } catch (error) {
      res.status(500).json({ message: "Failed to get bot status" });
    }
  });

  app.post("/api/bot/start", async (req, res) => {
    try {
      await sobertBot.start();
      res.json({ message: "Bot started successfully" });
    } catch (error) {
      res.status(500).json({ message: "Failed to start bot" });
    }
  });

  app.post("/api/bot/stop", async (req, res) => {
    try {
      sobertBot.stop();
      res.json({ message: "Bot stopped successfully" });
    } catch (error) {
      res.status(500).json({ message: "Failed to stop bot" });
    }
  });

  // Configuration routes
  app.get("/api/config", async (req, res) => {
    try {
      const config = await storage.getBotConfig();
      res.json(config);
    } catch (error) {
      res.status(500).json({ message: "Failed to get configuration" });
    }
  });

  app.patch("/api/config", async (req, res) => {
    try {
      const validatedConfig = insertBotConfigSchema.parse(req.body);
      const updatedConfig = await storage.updateBotConfig(validatedConfig);
      
      await storage.addRecentActivity({
        type: 'config',
        description: 'Configuration updated via dashboard',
        source: 'Web Dashboard'
      });
      
      res.json(updatedConfig);
    } catch (error) {
      res.status(400).json({ message: "Invalid configuration data" });
    }
  });

  // Stats routes
  app.get("/api/stats", async (req, res) => {
    try {
      const stats = await storage.getBotStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Failed to get statistics" });
    }
  });

  // Activity routes
  app.get("/api/activity", async (req, res) => {
    try {
      const limit = parseInt(req.query.limit as string) || 10;
      const activities = await storage.getRecentActivity(limit);
      res.json(activities);
    } catch (error) {
      res.status(500).json({ message: "Failed to get recent activity" });
    }
  });

  // Bot commands info
  app.get("/api/commands", async (req, res) => {
    const commands = [
      {
        command: "/help",
        description: "Display available commands and usage information",
        icon: "question",
        status: "active"
      },
      {
        command: "/stats",
        description: "Show bot statistics and usage data",
        icon: "chart-bar",
        status: "active"
      },
      {
        command: "/option_set",
        description: "Adjust reply_prob and sticker_prob settings",
        icon: "cog",
        status: "admin"
      }
    ];
    
    res.json(commands);
  });

  const httpServer = createServer(app);
  
  // Start the bot when server starts
  sobertBot.start().catch(error => {
    console.error('Failed to start Telegram bot on server startup:', error);
  });

  return httpServer;
}
