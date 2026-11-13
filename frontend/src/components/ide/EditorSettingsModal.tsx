import React from 'react';
import { X, Sliders, Shield, Lock, Eye, Key } from 'lucide-react';

export type PrivacyMode = 'local_only' | 'cloud_only' | 'hybrid';

interface EditorSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  privacyMode: PrivacyMode;
  onPrivacyModeChange: (mode: PrivacyMode) => void;
  aiProvider: string;
  onAiProviderChange: (provider: string) => void;
  fontSize: number;
  onFontSizeChange: (size: number) => void;
}

export const EditorSettingsModal: React.FC<EditorSettingsModalProps> = ({
  isOpen,
  onClose,
  privacyMode,
  onPrivacyModeChange,
  aiProvider,
  onAiProviderChange,
  fontSize,
  onFontSizeChange,
}) => {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg bg-slate-900 border border-slate-800 rounded-xl shadow-2xl overflow-hidden flex flex-col text-xs text-slate-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800 bg-slate-950">
          <div className="flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-indigo-400" />
            <h3 className="font-semibold text-sm text-slate-100">IDE & Privacy Configuration</h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-200">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-5 space-y-5">
          {/* Privacy & Cloud Transmission Control */}
          <div className="space-y-2">
            <label className="font-semibold text-slate-300 flex items-center space-x-1.5">
              <Shield className="w-3.5 h-3.5 text-amber-400" />
              <span>AI Data Transmission & Privacy Mode</span>
            </label>
            <p className="text-[11px] text-slate-400">
              Guarantees project source code is never transmitted to cloud LLM APIs without explicit authorization.
            </p>
            <div className="grid grid-cols-3 gap-2 pt-1">
              <button
                type="button"
                onClick={() => onPrivacyModeChange('local_only')}
                className={`p-2.5 rounded-lg border text-left transition-all ${
                  privacyMode === 'local_only'
                    ? 'border-emerald-500 bg-emerald-950/40 text-emerald-200'
                    : 'border-slate-800 bg-slate-950 hover:bg-slate-800/60 text-slate-400'
                }`}
              >
                <div className="font-semibold">Local-Only</div>
                <div className="text-[10px] text-slate-400 mt-0.5">Ollama local inference only</div>
              </button>

              <button
                type="button"
                onClick={() => onPrivacyModeChange('hybrid')}
                className={`p-2.5 rounded-lg border text-left transition-all ${
                  privacyMode === 'hybrid'
                    ? 'border-indigo-500 bg-indigo-950/40 text-indigo-200'
                    : 'border-slate-800 bg-slate-950 hover:bg-slate-800/60 text-slate-400'
                }`}
              >
                <div className="font-semibold">Hybrid Mode</div>
                <div className="text-[10px] text-slate-400 mt-0.5">Local analysis + cloud opt-in</div>
              </button>

              <button
                type="button"
                onClick={() => onPrivacyModeChange('cloud_only')}
                className={`p-2.5 rounded-lg border text-left transition-all ${
                  privacyMode === 'cloud_only'
                    ? 'border-purple-500 bg-purple-950/40 text-purple-200'
                    : 'border-slate-800 bg-slate-950 hover:bg-slate-800/60 text-slate-400'
                }`}
              >
                <div className="font-semibold">Cloud-Only</div>
                <div className="text-[10px] text-slate-400 mt-0.5">Gemini / OpenAI hosted API</div>
              </button>
            </div>
          </div>

          {/* AI Provider Selection */}
          <div className="space-y-2">
            <label className="font-semibold text-slate-300">Default AI Model Provider</label>
            <select
              value={aiProvider}
              onChange={(e) => onAiProviderChange(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
            >
              <option value="gemini">Google Gemini (Gemini 2.5 Flash / Pro)</option>
              <option value="openai">OpenAI (GPT-4o)</option>
              <option value="ollama">Ollama Local (Gemma 3 4B / DeepSeek)</option>
            </select>
          </div>

          {/* Editor Font Size */}
          <div className="space-y-2">
            <label className="font-semibold text-slate-300">Monaco Editor Font Size ({fontSize}px)</label>
            <input
              type="range"
              min={11}
              max={20}
              value={fontSize}
              onChange={(e) => onFontSizeChange(Number(e.target.value))}
              className="w-full accent-indigo-500 bg-slate-800 rounded-lg cursor-pointer"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-slate-800 bg-slate-950 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium transition-colors"
          >
            Apply & Close
          </button>
        </div>
      </div>
    </div>
  );
};

