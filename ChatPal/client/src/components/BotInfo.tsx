import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuery } from "@tanstack/react-query";

export default function BotInfo() {
  const { data: status, isLoading } = useQuery({
    queryKey: ['/api/bot/status'],
    refetchInterval: 30000, // Refresh every 30 seconds
  });

  if (isLoading) {
    return (
      <Card className="p-6 animate-pulse">
        <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded mb-4"></div>
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex justify-between">
              <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/3"></div>
              <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/4"></div>
            </div>
          ))}
        </div>
      </Card>
    );
  }

  const isOnline = status?.isRunning;

  return (
    <Card className="border border-slate-200 dark:border-slate-700 shadow-sm">
      <div className="p-6">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4 flex items-center">
          <i className="fas fa-info-circle text-blue-500 mr-3"></i>
          Bot Information
        </h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-700">
            <span className="text-sm text-slate-600 dark:text-slate-400">Username</span>
            <span className="text-sm font-mono text-slate-900 dark:text-slate-100" data-testid="text-bot-username">
              @Siege_Chat_Bot
            </span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-700">
            <span className="text-sm text-slate-600 dark:text-slate-400">AI Model</span>
            <span className="text-sm text-slate-900 dark:text-slate-100" data-testid="text-ai-model">
              Cohere Command-R
            </span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-700">
            <span className="text-sm text-slate-600 dark:text-slate-400">Personality</span>
            <span className="text-sm text-slate-900 dark:text-slate-100" data-testid="text-training-data">
              Harley Quinn Style
            </span>
          </div>
          
          <div className="flex justify-between items-center py-2 border-b border-slate-100 dark:border-slate-700">
            <span className="text-sm text-slate-600 dark:text-slate-400">Last Update</span>
            <span className="text-sm text-slate-900 dark:text-slate-100" data-testid="text-last-update">
              {status?.stats?.lastUpdateTime ? 
                new Date(status.stats.lastUpdateTime).toLocaleString() : 
                'Unknown'
              }
            </span>
          </div>
          
          <div className="flex justify-between items-center py-2">
            <span className="text-sm text-slate-600 dark:text-slate-400">Status</span>
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500' : 'bg-red-500'}`}></div>
              <span className={`text-sm font-medium ${isOnline ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`} data-testid="text-bot-status">
                {isOnline ? 'Online' : 'Offline'}
              </span>
            </div>
          </div>
        </div>
        
        <div className="mt-6 pt-4 border-t border-slate-200 dark:border-slate-700">
          <Button 
            asChild
            className="w-full bg-blue-500 hover:bg-blue-600 text-white"
            data-testid="button-open-telegram"
          >
            <a href="https://t.me/sobertbot" target="_blank" rel="noopener noreferrer">
              <i className="fab fa-telegram-plane mr-2"></i>
              Open in Telegram
            </a>
          </Button>
        </div>
      </div>
    </Card>
  );
}
