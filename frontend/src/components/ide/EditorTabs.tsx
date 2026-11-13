import React from 'react';
import { X, FileCode, Circle } from 'lucide-react';

export interface OpenFileTab {
  id: string;
  name: string;
  path: string;
  isModified?: boolean;
  language?: string;
}

interface EditorTabsProps {
  openTabs: OpenFileTab[];
  activeTabId: string | null;
  onSelectTab: (tabId: string) => void;
  onCloseTab: (tabId: string, e: React.MouseEvent) => void;
  onSplitEditor?: () => void;
  isSplitView?: boolean;
}

export const EditorTabs: React.FC<EditorTabsProps> = ({
  openTabs,
  activeTabId,
  onSelectTab,
  onCloseTab,
  onSplitEditor,
  isSplitView = false,
}) => {
  if (openTabs.length === 0) {
    return (
      <div className="h-9 bg-slate-950 border-b border-slate-800 flex items-center px-4 text-xs text-slate-500 italic select-none">
        No files open
      </div>
    );
  }

  return (
    <div className="h-9 bg-slate-950 border-b border-slate-800/80 flex items-center justify-between overflow-x-auto select-none no-scrollbar">
      <div className="flex items-center h-full">
        {openTabs.map((tab) => {
          const isActive = tab.id === activeTabId;
          return (
            <div
              key={tab.id}
              onClick={() => onSelectTab(tab.id)}
              className={`h-full flex items-center space-x-2 px-3 border-r border-slate-800/60 text-xs cursor-pointer group transition-colors ${
                isActive
                  ? 'bg-slate-900 text-slate-100 border-t-2 border-t-indigo-500 font-medium'
                  : 'bg-slate-950/60 text-slate-400 hover:bg-slate-900/40 hover:text-slate-300'
              }`}
            >
              <FileCode className={`w-3.5 h-3.5 ${isActive ? 'text-indigo-400' : 'text-slate-500'}`} />
              <span className="truncate max-w-[150px]" title={tab.path}>
                {tab.name}
              </span>

              {tab.isModified ? (
                <Circle className="w-2 h-2 text-indigo-400 fill-indigo-400" />
              ) : (
                <button
                  onClick={(e) => onCloseTab(tab.id, e)}
                  className="opacity-0 group-hover:opacity-100 hover:text-slate-100 p-0.5 rounded hover:bg-slate-800 transition-opacity"
                  title="Close Tab"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </div>
          );
        })}
      </div>

      {onSplitEditor && (
        <div className="flex items-center px-2 border-l border-slate-800/80 shrink-0">
          <button
            onClick={onSplitEditor}
            title={isSplitView ? 'Close Split View' : 'Split Editor Right'}
            className={`px-2 py-1 text-xs rounded transition-colors ${
              isSplitView
                ? 'text-indigo-400 bg-indigo-950/50'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
            }`}
          >
            {isSplitView ? 'Unsplit' : 'Split'}
          </button>
        </div>
      )}
    </div>
  );
};

