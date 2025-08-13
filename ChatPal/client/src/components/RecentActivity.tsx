import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuery } from "@tanstack/react-query";
import { type RecentActivity } from "@shared/schema";

export default function RecentActivity() {
  const { data: activities, isLoading } = useQuery<RecentActivity[]>({
    queryKey: ['/api/activity'],
    refetchInterval: 15000, // Refresh every 15 seconds
  });

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'response':
        return 'w-2 h-2 bg-emerald-500 rounded-full mt-2 flex-shrink-0';
      case 'message':
        return 'w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0';
      case 'group':
        return 'w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0';
      case 'config':
        return 'w-2 h-2 bg-amber-500 rounded-full mt-2 flex-shrink-0';
      default:
        return 'w-2 h-2 bg-slate-500 rounded-full mt-2 flex-shrink-0';
    }
  };

  const formatTimeAgo = (timestamp: string | Date) => {
    const now = new Date();
    const time = new Date(timestamp);
    const diffMs = now.getTime() - time.getTime();
    const diffMins = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMins / 60);

    if (diffMins < 1) return 'just now';
    if (diffMins < 60) return `${diffMins} mins ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    return time.toLocaleDateString();
  };

  if (isLoading) {
    return (
      <Card className="border border-slate-200 dark:border-slate-700 shadow-sm">
        <div className="p-6">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4 flex items-center">
            <i className="fas fa-clock text-blue-500 mr-3"></i>
            Recent Activity
          </h3>
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="flex items-start space-x-3 animate-pulse">
                <div className="w-2 h-2 bg-slate-300 rounded-full mt-2"></div>
                <div className="flex-1">
                  <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded mb-1"></div>
                  <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card className="border border-slate-200 dark:border-slate-700 shadow-sm">
      <div className="p-6">
        <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-4 flex items-center">
          <i className="fas fa-clock text-blue-500 mr-3"></i>
          Recent Activity
        </h3>
        
        <div className="space-y-4">
          {activities && activities.length > 0 ? (
            activities.map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3" data-testid={`activity-${activity.type}`}>
                <div className={getActivityIcon(activity.type)}></div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-slate-900 dark:text-slate-100">{activity.description}</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    {activity.source ? `${activity.source} • ` : ''}
                    {formatTimeAgo(activity.timestamp)}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-4 text-slate-500 dark:text-slate-400">
              No recent activity available.
            </div>
          )}
        </div>
        
        <Button 
          variant="ghost" 
          className="w-full mt-4 text-sm text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
          data-testid="button-view-all-activity"
        >
          View All Activity
          <i className="fas fa-arrow-right ml-1 text-xs"></i>
        </Button>
      </div>
    </Card>
  );
}
