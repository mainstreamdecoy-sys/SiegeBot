import { Card } from "@/components/ui/card";
import { useQuery } from "@tanstack/react-query";
import { type BotStats } from "@shared/schema";

export default function StatsOverview() {
  const { data: stats, isLoading } = useQuery<BotStats>({
    queryKey: ['/api/stats'],
  });

  if (isLoading) {
    return (
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-6">Bot Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="p-6 animate-pulse">
              <div className="h-12 bg-slate-200 dark:bg-slate-700 rounded mb-4"></div>
              <div className="h-8 bg-slate-200 dark:bg-slate-700 rounded mb-2"></div>
              <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded"></div>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-6">Bot Overview</h2>
        <div className="text-center py-8 text-slate-500">
          Failed to load statistics. Please try again later.
        </div>
      </div>
    );
  }

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100 mb-6">Bot Overview</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Total Messages</p>
              <p className="text-2xl font-bold text-slate-900 dark:text-slate-100" data-testid="stat-total-messages">
                {stats.totalMessages.toLocaleString()}
              </p>
            </div>
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-xl flex items-center justify-center">
              <i className="fas fa-comments text-blue-600 dark:text-blue-400"></i>
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <i className="fas fa-arrow-up text-emerald-500 mr-1"></i>
            <span className="text-emerald-600 dark:text-emerald-400 font-medium">+12.5%</span>
            <span className="text-slate-500 dark:text-slate-400 ml-1">this month</span>
          </div>
        </Card>
        
        <Card className="p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Active Groups</p>
              <p className="text-2xl font-bold text-slate-900 dark:text-slate-100" data-testid="stat-active-groups">
                {stats.activeGroups}
              </p>
            </div>
            <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-xl flex items-center justify-center">
              <i className="fas fa-users text-indigo-600 dark:text-indigo-400"></i>
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <i className="fas fa-arrow-up text-emerald-500 mr-1"></i>
            <span className="text-emerald-600 dark:text-emerald-400 font-medium">+8</span>
            <span className="text-slate-500 dark:text-slate-400 ml-1">new groups</span>
          </div>
        </Card>
        
        <Card className="p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">AI Model</p>
              <p className="text-2xl font-bold text-slate-900 dark:text-slate-100" data-testid="stat-ai-parameters">
                Cohere
              </p>
            </div>
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900 rounded-xl flex items-center justify-center">
              <i className="fas fa-brain text-purple-600 dark:text-purple-400"></i>
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-slate-600 dark:text-slate-400">Command-R</span>
          </div>
        </Card>
        
        <Card className="p-6 border border-slate-200 dark:border-slate-700 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 dark:text-slate-400">Response Rate</p>
              <p className="text-2xl font-bold text-slate-900 dark:text-slate-100" data-testid="stat-response-rate">
                {(stats.responseRate * 100).toFixed(1)}%
              </p>
            </div>
            <div className="w-12 h-12 bg-emerald-100 dark:bg-emerald-900 rounded-xl flex items-center justify-center">
              <i className="fas fa-chart-line text-emerald-600 dark:text-emerald-400"></i>
            </div>
          </div>
          <div className="mt-4 flex items-center text-sm">
            <span className="text-slate-600 dark:text-slate-400">Uptime</span>
          </div>
        </Card>
      </div>
    </div>
  );
}
