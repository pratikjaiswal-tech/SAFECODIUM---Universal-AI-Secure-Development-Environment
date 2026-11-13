import React, { useState } from 'react';
import { GitBranch, GitCommit, RefreshCw, Check, Diff, Plus, FileCode, CheckCircle2 } from 'lucide-react';

interface GitPanelProps {
  branchName?: string;
  modifiedFiles?: Array<{ path: string; status: 'modified' | 'added' | 'deleted' }>;
  onCommit?: (message: string) => void;
  onViewDiff?: (path: string) => void;
  onCreateBranch?: (branch: string) => void;
}

export const GitPanel: React.FC<GitPanelProps> = ({
  branchName = 'main',
  modifiedFiles = [],
  onCommit,
  onViewDiff,
  onCreateBranch,
}) => {
  const [commitMessage, setCommitMessage] = useState('');
  const [isCommitting, setIsCommitting] = useState(false);
  const [newBranchInput, setNewBranchInput] = useState('');
  const [showNewBranch, setShowNewBranch] = useState(false);

  const handleCommitSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!commitMessage.trim()) return;

    setIsCommitting(true);
    setTimeout(() => {
      if (onCommit) onCommit(commitMessage);
      setCommitMessage('');
      setIsCommitting(false);
    }, 400);
  };

  const handleCreateBranch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newBranchInput.trim()) return;
    if (onCreateBranch) onCreateBranch(newBranchInput.trim());
    setNewBranchInput('');
    setShowNewBranch(false);
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-300 text-xs">
      {/* Git Header */}
      <div className="p-3 border-b border-slate-800/80 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <GitBranch className="w-4 h-4 text-indigo-400" />
          <span className="font-semibold text-slate-200">Source Control</span>
          <span className="px-1.5 py-0.5 rounded bg-indigo-950/80 text-indigo-300 text-[10px] font-mono">
            {branchName}
          </span>
        </div>
        <button
          onClick={() => setShowNewBranch(!showNewBranch)}
          className="p-1 hover:text-slate-100 rounded hover:bg-slate-900 transition-colors"
          title="Create Isolated Repair Branch"
        >
          <Plus className="w-3.5 h-3.5" />
        </button>
      </div>

      {showNewBranch && (
        <form onSubmit={handleCreateBranch} className="p-3 border-b border-slate-800/80 bg-slate-900/50">
          <input
            type="text"
            value={newBranchInput}
            onChange={(e) => setNewBranchInput(e.target.value)}
            placeholder="Branch name (e.g. fix/cwe-120-patch)..."
            className="w-full bg-slate-950 border border-slate-700/80 rounded px-2.5 py-1 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 mb-2"
          />
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={() => setShowNewBranch(false)}
              className="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-2 py-0.5 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-medium"
            >
              Branch
            </button>
          </div>
        </form>
      )}

      {/* Commit Input Area */}
      <form onSubmit={handleCommitSubmit} className="p-3 border-b border-slate-800/80 flex flex-col space-y-2">
        <textarea
          rows={2}
          value={commitMessage}
          onChange={(e) => setCommitMessage(e.target.value)}
          placeholder="Commit message (e.g., 'Apply verified bounds patch')..."
          className="w-full bg-slate-900/80 border border-slate-800 rounded p-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500 resize-none font-mono"
        />
        <button
          type="submit"
          disabled={!commitMessage.trim() || isCommitting}
          className="w-full py-1.5 px-3 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-medium flex items-center justify-center space-x-1.5 disabled:opacity-40 transition-colors shadow-sm"
        >
          <GitCommit className="w-3.5 h-3.5" />
          <span>{isCommitting ? 'Committing...' : 'Commit to Branch'}</span>
        </button>
      </form>

      {/* Changed Files List */}
      <div className="flex-1 overflow-y-auto p-3">
        <div className="flex items-center justify-between text-[11px] text-slate-400 font-semibold mb-2 uppercase tracking-wider">
          <span>Changes ({modifiedFiles.length})</span>
        </div>

        {modifiedFiles.length === 0 ? (
          <div className="text-slate-500 italic py-4 text-center">
            No working tree changes detected
          </div>
        ) : (
          <div className="space-y-1">
            {modifiedFiles.map((file, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-1.5 rounded hover:bg-slate-900 group cursor-pointer transition-colors"
                onClick={() => onViewDiff && onViewDiff(file.path)}
              >
                <div className="flex items-center space-x-2 truncate">
                  <FileCode className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-400 shrink-0" />
                  <span className="truncate text-slate-300 font-mono text-[11px]">{file.path}</span>
                </div>
                <div className="flex items-center space-x-1 shrink-0">
                  <span
                    className={`text-[10px] font-bold px-1 rounded uppercase ${
                      file.status === 'modified'
                        ? 'text-amber-400'
                        : file.status === 'added'
                        ? 'text-emerald-400'
                        : 'text-rose-400'
                    }`}
                  >
                    {file.status === 'modified' ? 'M' : file.status === 'added' ? 'A' : 'D'}
                  </span>
                  <button
                    title="View Diff"
                    className="opacity-0 group-hover:opacity-100 p-0.5 hover:text-indigo-300"
                  >
                    <Diff className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

