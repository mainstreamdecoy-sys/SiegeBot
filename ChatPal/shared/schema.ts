import { sql } from "drizzle-orm";
import { pgTable, text, varchar, real, integer, boolean, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const botConfig = pgTable("bot_config", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  replyProbability: real("reply_probability").notNull().default(0.75),
  stickerProbability: real("sticker_probability").notNull().default(0.15),
  groupAutoRespond: boolean("group_auto_respond").notNull().default(true),
  mentionsOnly: boolean("mentions_only").notNull().default(false),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const botStats = pgTable("bot_stats", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  totalMessages: integer("total_messages").notNull().default(0),
  activeGroups: integer("active_groups").notNull().default(0),
  responseRate: real("response_rate").notNull().default(0),
  lastUpdateTime: timestamp("last_update_time").defaultNow(),
});

export const recentActivity = pgTable("recent_activity", {
  id: varchar("id").primaryKey().default(sql`gen_random_uuid()`),
  type: text("type").notNull(),
  description: text("description").notNull(),
  source: text("source"),
  timestamp: timestamp("timestamp").defaultNow(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertBotConfigSchema = createInsertSchema(botConfig).omit({
  id: true,
  updatedAt: true,
});

export const insertBotStatsSchema = createInsertSchema(botStats).omit({
  id: true,
  lastUpdateTime: true,
});

export const insertRecentActivitySchema = createInsertSchema(recentActivity).omit({
  id: true,
  timestamp: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type BotConfig = typeof botConfig.$inferSelect;
export type InsertBotConfig = z.infer<typeof insertBotConfigSchema>;
export type BotStats = typeof botStats.$inferSelect;
export type InsertBotStats = z.infer<typeof insertBotStatsSchema>;
export type RecentActivity = typeof recentActivity.$inferSelect;
export type InsertRecentActivity = z.infer<typeof insertRecentActivitySchema>;
