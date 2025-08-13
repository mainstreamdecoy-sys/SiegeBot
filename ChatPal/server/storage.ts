import { type User, type InsertUser, type BotConfig, type InsertBotConfig, type BotStats, type InsertBotStats, type RecentActivity, type InsertRecentActivity } from "@shared/schema";
import { randomUUID } from "crypto";

export interface IStorage {
  getUser(id: string): Promise<User | undefined>;
  getUserByUsername(username: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  
  getBotConfig(): Promise<BotConfig>;
  updateBotConfig(config: Partial<InsertBotConfig>): Promise<BotConfig>;
  
  getBotStats(): Promise<BotStats>;
  updateBotStats(stats: Partial<InsertBotStats>): Promise<BotStats>;
  incrementMessageCount(): Promise<void>;
  incrementGroupCount(): Promise<void>;
  updateResponseRate(): Promise<void>;
  
  getRecentActivity(limit?: number): Promise<RecentActivity[]>;
  addRecentActivity(activity: InsertRecentActivity): Promise<RecentActivity>;
}

export class MemStorage implements IStorage {
  private users: Map<string, User>;
  private botConfig: BotConfig;
  private botStats: BotStats;
  private activities: RecentActivity[];
  private totalResponses: number = 0;

  constructor() {
    this.users = new Map();
    this.activities = [];
    
    // Initialize default bot configuration
    this.botConfig = {
      id: randomUUID(),
      replyProbability: 0.75,
      stickerProbability: 0.15,
      groupAutoRespond: true,
      mentionsOnly: false,
      updatedAt: new Date(),
    };

    // Initialize default bot stats
    this.botStats = {
      id: randomUUID(),
      totalMessages: 1247892,
      activeGroups: 186,
      responseRate: 0.942,
      lastUpdateTime: new Date(),
    };

    // Initialize some recent activity
    this.activities = [
      {
        id: randomUUID(),
        type: 'response',
        description: 'Responded in group chat',
        source: 'Tech Enthusiasts',
        timestamp: new Date(Date.now() - 2 * 60 * 1000), // 2 mins ago
      },
      {
        id: randomUUID(),
        type: 'message',
        description: 'Private message received',
        source: 'User_12345',
        timestamp: new Date(Date.now() - 8 * 60 * 1000), // 8 mins ago
      },
      {
        id: randomUUID(),
        type: 'group',
        description: 'Added to new group',
        source: 'Developer Community',
        timestamp: new Date(Date.now() - 15 * 60 * 1000), // 15 mins ago
      },
      {
        id: randomUUID(),
        type: 'config',
        description: 'Configuration updated',
        source: 'Reply probability',
        timestamp: new Date(Date.now() - 60 * 60 * 1000), // 1 hour ago
      },
    ];
  }

  async getUser(id: string): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByUsername(username: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(
      (user) => user.username === username,
    );
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const id = randomUUID();
    const user: User = { ...insertUser, id };
    this.users.set(id, user);
    return user;
  }

  async getBotConfig(): Promise<BotConfig> {
    return { ...this.botConfig };
  }

  async updateBotConfig(config: Partial<InsertBotConfig>): Promise<BotConfig> {
    this.botConfig = {
      ...this.botConfig,
      ...config,
      updatedAt: new Date(),
    };
    return { ...this.botConfig };
  }

  async getBotStats(): Promise<BotStats> {
    return { ...this.botStats };
  }

  async updateBotStats(stats: Partial<InsertBotStats>): Promise<BotStats> {
    this.botStats = {
      ...this.botStats,
      ...stats,
      lastUpdateTime: new Date(),
    };
    return { ...this.botStats };
  }

  async incrementMessageCount(): Promise<void> {
    this.botStats.totalMessages += 1;
    this.botStats.lastUpdateTime = new Date();
  }

  async incrementGroupCount(): Promise<void> {
    this.botStats.activeGroups += 1;
    this.botStats.lastUpdateTime = new Date();
  }

  async updateResponseRate(): Promise<void> {
    this.totalResponses += 1;
    // Calculate response rate as responses / total messages
    this.botStats.responseRate = Math.min(1, this.totalResponses / this.botStats.totalMessages);
    this.botStats.lastUpdateTime = new Date();
  }

  async getRecentActivity(limit: number = 10): Promise<RecentActivity[]> {
    return this.activities
      .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
      .slice(0, limit);
  }

  async addRecentActivity(activity: InsertRecentActivity): Promise<RecentActivity> {
    const newActivity: RecentActivity = {
      ...activity,
      id: randomUUID(),
      timestamp: new Date(),
    };
    
    this.activities.unshift(newActivity);
    
    // Keep only the last 50 activities
    if (this.activities.length > 50) {
      this.activities = this.activities.slice(0, 50);
    }
    
    return newActivity;
  }
}

export const storage = new MemStorage();
