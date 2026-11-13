import React from 'react';
import { AlertTriangle, AlertCircle, Info, CheckCircle2, ChevronRight, FileCode } from 'lucide-react';
import { VulnerabilityData } from '../../services/api';

interface DiagnosticsPanelProps {
  findings: VulnerabilityData[];
  onSelectFinding: (vuln: VulnerabilityData) => void;
  selectedFindingId?: string | null;
}

export const DiagnosticsPanel: React.FC<DiagnosticsPanelProps> = ({
  findings,
  onSelectFinding,
  selectedFindingId,
}) => {
  const criticalCount = findings.filter((f) => f.severity === 'CRITICAL').length;
  const highCount = findings.filter((f) => f.severity === 'HIGH').length;
  const mediumCount = findings.filter((f) => f.severity === 'MEDIUM').length;

  return (
    <div className="flex flex-col h-full bg-[#090d16] text-xs">
      {/* Summary Header */}
      <div className="h-7 bg-slate-950 px-3 flex items-center justify-between border-b border-slate-800/80 text-[11px] select-none">
        <div className="flex items-center space-x-3 text-slate-400">
          <span>Problems & Diagnostics ({findings.length})</span>
          {criticalCount > 0 && (
            <span className="flex items-center space-x-1 text-rose-400 font-semibold">
              <AlertCircle className="w-3 h-3" />
              <span>{criticalCount} Critical</span>
            </span>
          )}
          {highCount > 0 && (
            <span className="flex items-center space-x-1 text-amber-400 font-semibold">
              <AlertTriangle className="w-3 h-3" />
              <span>{highCount} High</span>
            </span>
          )}
          {mediumCount > 0 && (
            <span className="flex items-center space-x-1 text-yellow-300">
              <Info className="w-3 h-3" />
              <span>{mediumCount} Medium</span>
            </span>
          )}
        </div>
      </div>

      {/* Diagnostics List */}
      <div className="flex-1 overflow-y-auto p-2">
        {findings.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-500 py-6">
            <CheckCircle2 className="w-8 h-8 text-emerald-500 mb-2 opacity-60" />
            <p className="font-medium text-slate-400">No active code diagnostics or CWE violations detected.</p>
            <p className="text-[11px] text-slate-500 mt-1">Run a full security audit to analyze workspace files.</p>
          </div>
        ) : (
          <div className="space-y-1">
            {findings.map((item) => {
              const isSelected = item.id === selectedFindingId;
              const isCrit = item.severity === 'CRITICAL';
              const isHigh = item.severity === 'HIGH';

              return (
                <div
                  key={item.id}
                  onClick={() => onSelectFinding(item)}
                  className={`flex items-start space-x-2 p-2 rounded cursor-pointer transition-colors border ${
                    isSelected
                      ? 'bg-slate-900 border-indigo-500/60'
                      : 'border-transparent hover:bg-slate-900/60'
                  }`}
                >
                  <div className="mt-0.5 shrink-0">
                    {isCrit ? (
                      <AlertCircle className="w-4 h-4 text-rose-400" />
                    ) : isHigh ? (
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                    ) : (
                      <Info className="w-4 h-4 text-blue-400" />
                    )}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold text-slate-200 truncate">{item.title}</span>
                      <span className="px-1.5 py-0.2 bg-slate-800 text-indigo-300 rounded text-[10px] font-mono">
                        {item.cwe_id}
                      </span>
                      <span
                        className={`text-[9px] font-bold px-1 rounded uppercase ${
                          isCrit
                            ? 'bg-rose-950/80 text-rose-400'
                            : isHigh
                            ? 'bg-amber-950/80 text-amber-400'
                            : 'bg-blue-950/80 text-blue-400'
                        }`}
                      >
                        {item.severity}
                      </span>
                    </div>

                    <div className="flex items-center space-x-2 mt-1 text-slate-400 text-[11px]">
                      <FileCode className="w-3 h-3 text-slate-500" />
                      <span className="font-mono text-slate-300">{item.file_path}</span>
                      <span>line {item.line_start}</span>
                      {item.function_name && (
                        <span className="text-slate-500 font-mono">in {item.function_name}()</span>
                      )}
                    </div>
                  </div>

                  <ChevronRight className="w-4 h-4 text-slate-600 mt-1 shrink-0" />
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

