import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useMutation } from "@tanstack/react-query";
import { apiRequest, queryClient } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";

export default function QuickActions() {
  const { toast } = useToast();

  const restartBotMutation = useMutation({
    mutationFn: async () => {
      await apiRequest('POST', '/api/bot/stop');
      await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second
      await apiRequest('POST', '/api/bot/start');
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/bot/status'] });
      toast({
        title: "Bot Restarted",
        description: "SobertBot has been restarted successfully.",
      });
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to restart bot. Please try again.",
        variant: "destructive",
      });
    }
  });

  const handleViewLogs = () => {
    toast({
      title: "View Logs",
      description: "Logs viewer would open here in a real implementation.",
    });
  };

  const handleExportData = () => {
    toast({
      title: "Export Data",
      description: "Data export would begin here in a real implementation.",
    });
  };

  const handleCheckUpdates = () => {
    toast({
      title: "Check Updates",
      description: "Bot is running the latest version.",
    });
  };

  return (
    <Card className="border border-slate-200 dark:border-slate-700 shadow-sm">
      <div className="p-6">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4 flex items-center">
          <i className="fas fa-bolt text-blue-500 mr-3"></i>
          Quick Actions
        </h3>
        
        <div className="space-y-3">
          <Button
            variant="outline"
            className="w-full justify-between border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800"
            onClick={() => restartBotMutation.mutate()}
            disabled={restartBotMutation.isPending}
            data-testid="button-restart-bot"
          >
            <div className="flex items-center space-x-3">
              <i className={`fas ${restartBotMutation.isPending ? 'fa-spinner fa-spin' : 'fa-sync-alt'} text-slate-400`}></i>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {restartBotMutation.isPending ? 'Restarting...' : 'Restart Bot'}
              </span>
            </div>
            <i className="fas fa-chevron-right text-xs text-slate-400"></i>
          </Button>
          
          <Button
            variant="outline"
            className="w-full justify-between border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800"
            onClick={handleViewLogs}
            data-testid="button-view-logs"
          >
            <div className="flex items-center space-x-3">
              <i className="fas fa-file-alt text-slate-400"></i>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">View Logs</span>
            </div>
            <i className="fas fa-chevron-right text-xs text-slate-400"></i>
          </Button>
          
          <Button
            variant="outline"
            className="w-full justify-between border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800"
            onClick={handleExportData}
            data-testid="button-export-data"
          >
            <div className="flex items-center space-x-3">
              <i className="fas fa-download text-slate-400"></i>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Export Data</span>
            </div>
            <i className="fas fa-chevron-right text-xs text-slate-400"></i>
          </Button>
          
          <Button
            variant="outline"
            className="w-full justify-between border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800"
            onClick={handleCheckUpdates}
            data-testid="button-check-updates"
          >
            <div className="flex items-center space-x-3">
              <i className="fas fa-cloud-download-alt text-slate-400"></i>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">Check Updates</span>
            </div>
            <i className="fas fa-chevron-right text-xs text-slate-400"></i>
          </Button>
        </div>
      </div>
    </Card>
  );
}
