import { useQuery } from "@tanstack/react-query";
import StatsOverview from "@/components/StatsOverview";
import ConfigurationPanel from "@/components/ConfigurationPanel";
import BotInfo from "@/components/BotInfo";
import RecentActivity from "@/components/RecentActivity";
import QuickActions from "@/components/QuickActions";

export default function Dashboard() {
  const { data: status } = useQuery({
    queryKey: ['/api/bot/status'],
    refetchInterval: 30000,
  });

  const isOnline = status?.isRunning;

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 font-inter">
      {/* Header */}
      <header className="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
                  <i className="fas fa-robot text-white text-lg"></i>
                </div>
                <div>
                  <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100">SobertBot</h1>
                  <p className="text-sm text-slate-500 dark:text-slate-400">AI Telegram Bot Dashboard</p>
                </div>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* Bot Status Indicator */}
              <div className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
                isOnline ? 'bg-emerald-50 dark:bg-emerald-900' : 'bg-red-50 dark:bg-red-900'
              }`} data-testid="status-indicator">
                <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
                <span className={`text-sm font-medium ${
                  isOnline ? 'text-emerald-700 dark:text-emerald-400' : 'text-red-700 dark:text-red-400'
                }`}>
                  {isOnline ? 'Online' : 'Offline'}
                </span>
              </div>
              
              <button className="p-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors" data-testid="button-notifications">
                <i className="fas fa-bell"></i>
              </button>
              
              <button className="p-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-lg transition-colors" data-testid="button-settings">
                <i className="fas fa-cog"></i>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <StatsOverview />

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <ConfigurationPanel />
          
          {/* Side Panel */}
          <div className="space-y-6">
            <BotInfo />
            <RecentActivity />
            <QuickActions />
          </div>
        </div>
      </div>
    </div>
  );
}
