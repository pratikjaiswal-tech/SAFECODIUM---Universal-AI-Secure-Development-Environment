import React from 'react';
import {
  Files,
  Search,
  GitBranch,
  ShieldAlert,
  Bot,
  Terminal,
  Settings,
  HelpCircle,
  Play,
  RotateCcw
} from 'lucide-react';

export type ActivityBarTab = 'explorer' | 'search' | 'git' | 'security' | 'ai' | 'settings';

interface ActivityBarProps {
  activeTab: ActivityBarTab;
  onTabSelect: (tab: ActivityBarTab) => void;
  isSidebarOpen: boolean;
  onToggleSidebar: () => void;
  findingsCount?: number;
  onRunAudit?: () => void;
  isRunningAudit?: boolean;
}

export const ActivityBar: React.FC<ActivityBarProps> = ({
  activeTab,
  onTabSelect,
  isSidebarOpen,
  onToggleSidebar,
  findingsCount = 0,
  onRunAudit,
  isRunningAudit = false,
}) => {
  const handleTabClick = (tab: ActivityBarTab) => {
    if (activeTab === tab && isSidebarOpen) {
      onToggleSidebar();
    } else {
      onTabSelect(tab);
      if (!isSidebarOpen) {
        onToggleSidebar();
      }
    }
  };

  return (
    <aside className="w-12 bg-slate-950 border-r border-slate-800/80 flex flex-col items-center py-3 select-none z-30 shrink-0">
      {/* Top Branding / Mode Icon */}
      <div className="mb-4">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-xs shadow-md shadow-indigo-500/20">
          SC
        </div>
      </div>

      {/* Main Activity Views */}
      <div className="flex-1 flex flex-col space-y-1 w-full items-center">
        <button
          onClick={() => handleTabClick('explorer')}
          title="Explorer (Ctrl+Shift+E)"
          className={`relative p-2.5 rounded-lg transition-colors ${
            activeTab === 'explorer' && isSidebarOpen
              ? 'text-indigo-400 bg-slate-900 border-l-2 border-indigo-500 rounded-l-none'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
          }`}
        >
          <Files className="w-5 h-5" />
        </button>

        <button
          onClick={() => handleTabClick('search')}
          title="Search Workspace (Ctrl+Shift+F)"
          className={`relative p-2.5 rounded-lg transition-colors ${
            activeTab === 'search' && isSidebarOpen
              ? 'text-indigo-400 bg-slate-900 border-l-2 border-indigo-500 rounded-l-none'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
          }`}
        >
          <Search className="w-5 h-5" />
        </button>

        <button
          onClick={() => handleTabClick('git')}
          title="Source Control / Git (Ctrl+Shift+G)"
          className={`relative p-2.5 rounded-lg transition-colors ${
            activeTab === 'git' && isSidebarOpen
              ? 'text-indigo-400 bg-slate-900 border-l-2 border-indigo-500 rounded-l-none'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
          }`}
        >
          <GitBranch className="w-5 h-5" />
        </button>

        <button
          onClick={() => handleTabClick('security')}
          title="Security Center & CWE Diagnostics (Ctrl+Shift+S)"
          className={`relative p-2.5 rounded-lg transition-colors ${
            activeTab === 'security' && isSidebarOpen
              ? 'text-amber-400 bg-slate-900 border-l-2 border-amber-500 rounded-l-none'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
          }`}
        >
          <ShieldAlert className="w-5 h-5" />
          {findingsCount > 0 && (
            <span className="absolute top-1 right-1 px-1.5 py-0.2 text-[9px] font-bold bg-amber-500 text-slate-950 rounded-full animate-pulse">
              {findingsCount}
            </span>
          )}
        </button>

        <button
          onClick={() => handleTabClick('ai')}
          title="AI Assistant & VibeChat (Ctrl+Shift+A)"
          className={`relative p-2.5 rounded-lg transition-colors ${
            activeTab === 'ai' && isSidebarOpen
              ? 'text-purple-400 bg-slate-900 border-l-2 border-purple-500 rounded-l-none'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
          }`}
        >
          <Bot className="w-5 h-5" />
        </button>

        {onRunAudit && (
          <div className="pt-2">
            <button
              onClick={onRunAudit}
              disabled={isRunningAudit}
              title="Run Security Audit Pipeline"
              className="p-2.5 rounded-lg text-emerald-400 hover:text-emerald-300 hover:bg-emerald-950/40 transition-colors disabled:opacity-50"
            >
              {isRunningAudit ? (
                <RotateCcw className="w-5 h-5 animate-spin" />
              ) : (
                <Play className="w-5 h-5 fill-emerald-500/20" />
              )}
            </button>
          </div>
        )}
      </div>

      {/* Bottom Auxiliary Controls */}
      <div className="flex flex-col space-y-1 w-full items-center pt-3 border-t border-slate-900">
        <button
          onClick={() => handleTabClick('settings')}
          title="IDE Settings & Privacy Config"
          className={`p-2.5 rounded-lg transition-colors ${
            activeTab === 'settings' && isSidebarOpen
              ? 'text-indigo-400 bg-slate-900'
              : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
          }`}
        >
          <Settings className="w-5 h-5" />
        </button>
      </div>
    </aside>
  );
};

