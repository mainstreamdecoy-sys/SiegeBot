import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useQuery, useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { apiRequest, queryClient } from "@/lib/queryClient";
import { useToast } from "@/hooks/use-toast";
import { type BotConfig } from "@shared/schema";

export default function ConfigurationPanel() {
  const { toast } = useToast();
  const [replyProb, setReplyProb] = useState(0.75);
  const [stickerProb, setStickerProb] = useState(0.15);
  const [groupAutoRespond, setGroupAutoRespond] = useState(true);
  const [mentionsOnly, setMentionsOnly] = useState(false);

  const { data: config, isLoading } = useQuery<BotConfig>({
    queryKey: ['/api/config'],
    onSuccess: (data) => {
      setReplyProb(data.replyProbability);
      setStickerProb(data.stickerProbability);
      setGroupAutoRespond(data.groupAutoRespond);
      setMentionsOnly(data.mentionsOnly);
    }
  });

  const { data: commands } = useQuery({
    queryKey: ['/api/commands'],
  });

  const updateConfigMutation = useMutation({
    mutationFn: async (newConfig: Partial<BotConfig>) => {
      const response = await apiRequest('PATCH', '/api/config', newConfig);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/config'] });
      queryClient.invalidateQueries({ queryKey: ['/api/activity'] });
      toast({
        title: "Configuration Updated",
        description: "Bot configuration has been saved successfully.",
      });
    },
    onError: () => {
      toast({
        title: "Error",
        description: "Failed to update configuration. Please try again.",
        variant: "destructive",
      });
    }
  });

  const handleSaveConfiguration = () => {
    updateConfigMutation.mutate({
      replyProbability: replyProb,
      stickerProbability: stickerProb,
      groupAutoRespond,
      mentionsOnly,
    });
  };

  if (isLoading) {
    return (
      <div className="lg:col-span-2 space-y-6">
        <Card className="p-6 animate-pulse">
          <div className="h-6 bg-slate-200 dark:bg-slate-700 rounded mb-4"></div>
          <div className="space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-16 bg-slate-200 dark:bg-slate-700 rounded"></div>
            ))}
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="lg:col-span-2 space-y-6">
      {/* Bot Configuration Card */}
      <Card className="border border-slate-200 dark:border-slate-700 shadow-sm">
        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center">
            <i className="fas fa-sliders-h text-blue-500 mr-3"></i>
            Bot Configuration
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">Adjust bot behavior and response patterns</p>
        </div>
        
        <div className="p-6 space-y-6">
          {/* Reply Probability */}
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Reply Probability</label>
              <span className="text-sm text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded" data-testid="reply-prob-value">
                {replyProb.toFixed(2)}
              </span>
            </div>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.1" 
              value={replyProb}
              onChange={(e) => setReplyProb(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
              data-testid="slider-reply-prob"
            />
            <p className="text-xs text-slate-500 dark:text-slate-400">Controls how often the bot replies to messages (0.0 = never, 1.0 = always)</p>
          </div>
          
          {/* Sticker Probability */}
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Sticker Probability</label>
              <span className="text-sm text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded" data-testid="sticker-prob-value">
                {stickerProb.toFixed(2)}
              </span>
            </div>
            <input 
              type="range" 
              min="0" 
              max="1" 
              step="0.05" 
              value={stickerProb}
              onChange={(e) => setStickerProb(parseFloat(e.target.value))}
              className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
              data-testid="slider-sticker-prob"
            />
            <p className="text-xs text-slate-500 dark:text-slate-400">Frequency of sending stickers in responses (disabled by default in groups)</p>
          </div>
          
          {/* Group Settings */}
          <div className="space-y-4">
            <h4 className="text-sm font-semibold text-slate-800 dark:text-slate-200">Group Chat Settings</h4>
            
            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <div className="flex items-center space-x-3">
                <i className="fas fa-users text-slate-400"></i>
                <div>
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-300">Auto-respond in Groups</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Enable automatic responses in group chats</p>
                </div>
              </div>
              <button 
                onClick={() => setGroupAutoRespond(!groupAutoRespond)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  groupAutoRespond ? 'bg-blue-500' : 'bg-slate-300 dark:bg-slate-600'
                }`}
                data-testid="toggle-group-auto-respond"
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  groupAutoRespond ? 'translate-x-6' : 'translate-x-1'
                }`}></span>
              </button>
            </div>
            
            <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-lg">
              <div className="flex items-center space-x-3">
                <i className="fas fa-reply text-slate-400"></i>
                <div>
                  <p className="text-sm font-medium text-slate-700 dark:text-slate-300">Reply to Mentions Only</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Only respond when directly mentioned or replied to</p>
                </div>
              </div>
              <button 
                onClick={() => setMentionsOnly(!mentionsOnly)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  mentionsOnly ? 'bg-blue-500' : 'bg-slate-300 dark:bg-slate-600'
                }`}
                data-testid="toggle-mentions-only"
              >
                <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  mentionsOnly ? 'translate-x-6' : 'translate-x-1'
                }`}></span>
              </button>
            </div>
          </div>
          
          {/* Save Button */}
          <div className="flex justify-end pt-4 border-t border-slate-200 dark:border-slate-700">
            <Button 
              onClick={handleSaveConfiguration}
              disabled={updateConfigMutation.isPending}
              className="bg-blue-500 hover:bg-blue-600 text-white"
              data-testid="button-save-config"
            >
              {updateConfigMutation.isPending ? (
                <>
                  <i className="fas fa-spinner fa-spin mr-2"></i>
                  Saving...
                </>
              ) : (
                <>
                  <i className="fas fa-save mr-2"></i>
                  Save Changes
                </>
              )}
            </Button>
          </div>
        </div>
      </Card>
      
      {/* Commands Management */}
      <Card className="border border-slate-200 dark:border-slate-700 shadow-sm">
        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
          <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 flex items-center">
            <i className="fas fa-terminal text-blue-500 mr-3"></i>
            Bot Commands
          </h3>
          <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">Available commands and their usage</p>
        </div>
        
        <div className="p-6">
          <div className="space-y-4">
            {commands?.map((command: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-4 border border-slate-200 dark:border-slate-700 rounded-lg">
                <div className="flex items-center space-x-4">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    command.icon === 'question' ? 'bg-blue-100 dark:bg-blue-900' :
                    command.icon === 'chart-bar' ? 'bg-purple-100 dark:bg-purple-900' :
                    'bg-amber-100 dark:bg-amber-900'
                  }`}>
                    <i className={`fas fa-${command.icon} ${
                      command.icon === 'question' ? 'text-blue-600 dark:text-blue-400' :
                      command.icon === 'chart-bar' ? 'text-purple-600 dark:text-purple-400' :
                      'text-amber-600 dark:text-amber-400'
                    }`}></i>
                  </div>
                  <div>
                    <code className="text-sm font-mono bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded text-blue-600 dark:text-blue-400">
                      {command.command}
                    </code>
                    <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">{command.description}</p>
                  </div>
                </div>
                <span className={`text-xs px-2 py-1 rounded ${
                  command.status === 'active' ? 'text-emerald-600 dark:text-emerald-400 bg-emerald-100 dark:bg-emerald-900' :
                  'text-amber-600 dark:text-amber-400 bg-amber-100 dark:bg-amber-900'
                }`}>
                  {command.status === 'active' ? 'Active' : 'Admin Only'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
}
