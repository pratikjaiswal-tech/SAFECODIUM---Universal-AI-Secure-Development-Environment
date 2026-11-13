import React, { useState } from 'react';
import {
  Shield,
  ShieldCheck,
  ShieldAlert,
  Play,
  RotateCcw,
  ExternalLink,
  Layers,
  FileCheck2,
  Cpu,
  Lock,
  Download
} from 'lucide-react';
import { VulnerabilityData, VerificationPassportData } from '../../services/api';

interface SecurityCenterPanelProps {
  findings: VulnerabilityData[];
  passport?: VerificationPassportData | null;
  onRunAudit: () => void;
  isRunningAudit: boolean;
  onSelectFinding: (vuln: VulnerabilityData) => void;
}

export const SecurityCenterPanel: React.FC<SecurityCenterPanelProps> = ({
  findings,
  passport,
  onRunAudit,
  isRunningAudit,
  onSelectFinding,
}) => {
  const criticalCount = findings.filter((f) => f.severity === 'CRITICAL').length;
  const highCount = findings.filter((f) => f.severity === 'HIGH').length;
  const verifiedCount = findings.filter((f) => f.status === 'verified').length;

  return (
    <div className="flex flex-col h-full bg-slate-950 text-slate-300 text-xs overflow-y-auto p-4 space-y-4">
      {/* Title & Audit Launcher */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800/80">
        <div className="flex items-center space-x-2">
          <Shield className="w-5 h-5 text-amber-400" />
          <div>
            <h2 className="font-bold text-slate-100 text-sm">Security Center</h2>
            <p className="text-[11px] text-slate-400">Deterministic Security & CWE Verification Hub</p>
          </div>
        </div>
        <button
          onClick={onRunAudit}
          disabled={isRunningAudit}
          className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-medium shadow-md shadow-indigo-500/20 disabled:opacity-50 transition-all text-xs"
        >
          {isRunningAudit ? (
            <>
              <RotateCcw className="w-3.5 h-3.5 animate-spin" />
              <span>Scanning...</span>
            </>
          ) : (
            <>
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>Scan Workspace</span>
            </>
          )}
        </button>
      </div>

      {/* Security Health Scorecard */}
      <div className="grid grid-cols-3 gap-2">
        <div className="p-3 bg-slate-900/80 border border-slate-800 rounded-lg flex flex-col items-center justify-center">
          <span className="text-xl font-bold text-slate-100">{findings.length}</span>
          <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Total Findings</span>
        </div>
        <div className="p-3 bg-slate-900/80 border border-slate-800 rounded-lg flex flex-col items-center justify-center">
          <span className="text-xl font-bold text-rose-400">{criticalCount + highCount}</span>
          <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Crit / High</span>
        </div>
        <div className="p-3 bg-slate-900/80 border border-slate-800 rounded-lg flex flex-col items-center justify-center">
          <span className="text-xl font-bold text-emerald-400">{verifiedCount}</span>
          <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Verified Repairs</span>
        </div>
      </div>

      {/* Verification Passport Status */}
      {passport && (
        <div className="p-3 bg-slate-900/60 border border-emerald-500/30 rounded-lg space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
              <span className="font-semibold text-emerald-300">Deterministic Security Passport</span>
            </div>
            <span className="px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-mono text-[10px]">
              {passport.final_status}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed">
            Patches independently compiled and verified with ASan/UBSan memory sanitizers. Zero unverified claims permitted.
          </p>
        </div>
      )}

      {/* Active CWE Findings List */}
      <div className="space-y-2">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
          Detected Vulnerabilities
        </span>

        {findings.length === 0 ? (
          <div className="p-4 bg-slate-900/40 border border-slate-800/60 rounded-lg text-center text-slate-500 italic">
            No vulnerabilities detected in active project workspace.
          </div>
        ) : (
          <div className="space-y-1.5">
            {findings.map((vuln) => (
              <div
                key={vuln.id}
                onClick={() => onSelectFinding(vuln)}
                className="p-2.5 bg-slate-900/70 border border-slate-800 hover:border-indigo-500/50 rounded-lg cursor-pointer transition-colors flex items-start justify-between"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-slate-200">{vuln.cwe_id}</span>
                    <span
                      className={`text-[9px] font-bold px-1.5 py-0.2 rounded uppercase ${
                        vuln.severity === 'CRITICAL'
                          ? 'bg-rose-950 text-rose-400'
                          : vuln.severity === 'HIGH'
                          ? 'bg-amber-950 text-amber-400'
                          : 'bg-blue-950 text-blue-400'
                      }`}
                    >
                      {vuln.severity}
                    </span>
                  </div>
                  <p className="text-slate-300 text-[11px] font-medium mt-0.5">{vuln.title}</p>
                  <p className="text-slate-500 text-[10px] font-mono mt-1">
                    {vuln.file_path}:{vuln.line_start}
                  </p>
                </div>
                <div className="flex flex-col items-end space-y-1">
                  <span
                    className={`text-[9px] font-mono px-1.5 py-0.5 rounded ${
                      vuln.status === 'verified'
                        ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30'
                        : 'bg-slate-800 text-slate-400'
                    }`}
                  >
                    {vuln.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
