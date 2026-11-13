import React, { useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';
import { Trash2, Terminal as TerminalIcon } from 'lucide-react';

interface TerminalPanelProps {
  onCommand?: (command: string) => void;
  height?: number;
}

export const TerminalPanel: React.FC<TerminalPanelProps> = ({ onCommand }) => {
  const terminalRef = useRef<HTMLDivElement | null>(null);
  const xtermInstance = useRef<Terminal | null>(null);
  const fitAddonInstance = useRef<FitAddon | null>(null);

  useEffect(() => {
    if (!terminalRef.current) return;

    // Create xterm terminal instance
    const term = new Terminal({
      cursorBlink: true,
      theme: {
        background: '#090d16',
        foreground: '#e2e8f0',
        cursor: '#6366f1',
        selectionBackground: '#312e81',
        black: '#0f172a',
        red: '#ef4444',
        green: '#10b981',
        yellow: '#f59e0b',
        blue: '#3b82f6',
        magenta: '#a855f7',
        cyan: '#06b6d4',
        white: '#f8fafc',
      },
      fontSize: 12,
      fontFamily: 'Consolas, "Fira Code", monospace',
      lineHeight: 1.2,
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(terminalRef.current);
    fitAddon.fit();

    xtermInstance.current = term;
    fitAddonInstance.current = fitAddon;

    term.writeln('\x1b[1;34m[SAFECODIUM IDE Terminal]\x1b[0m');
    term.writeln('\x1b[38;5;244mUniversal Secure Execution Shell (Emulated/Local)\x1b[0m');
    term.writeln('Type \x1b[32mhelp\x1b[0m or \x1b[32mscan\x1b[0m to interact with the workspace.\r\n');
    term.write('\x1b[32msafecodium-env$\x1b[0m ');

    let currentLine = '';

    term.onData((data) => {
      // Enter
      if (data === '\r') {
        term.write('\r\n');
        const trimmed = currentLine.trim();
        if (trimmed) {
          handleExecute(trimmed, term);
        }
        currentLine = '';
        term.write('\x1b[32msafecodium-env$\x1b[0m ');
      }
      // Backspace
      else if (data === '\u007F') {
        if (currentLine.length > 0) {
          currentLine = currentLine.slice(0, -1);
          term.write('\b \b');
        }
      }
      // Printable characters
      else if (data >= ' ' && data <= '~') {
        currentLine += data;
        term.write(data);
      }
    });

    const handleResize = () => {
      try {
        fitAddon.fit();
      } catch (e) {
        // Ignore resize during tab switches
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      term.dispose();
    };
  }, []);

  const handleExecute = (cmd: string, term: Terminal) => {
    if (onCommand) {
      onCommand(cmd);
    }

    if (cmd === 'clear') {
      term.clear();
      return;
    }

    if (cmd === 'help') {
      term.writeln('Available Built-in Commands:');
      term.writeln('  \x1b[33mscan\x1b[0m       - Run full vulnerability and AST static security scans');
      term.writeln('  \x1b[33mverify\x1b[0m     - Trigger compiler, ASan, and regression verification');
      term.writeln('  \x1b[33mls\x1b[0m         - List workspace files and directories');
      term.writeln('  \x1b[33mclear\x1b[0m      - Clear terminal screen');
      term.writeln('  \x1b[33mstatus\x1b[0m     - Show active project and security health status');
      return;
    }

    if (cmd === 'ls') {
      term.writeln('src/  include/  tests/  Makefile  firmware.c');
      return;
    }

    if (cmd === 'status') {
      term.writeln('\x1b[32mActive Workspace: Connected\x1b[0m');
      term.writeln('Sandboxing: Enabled (non-root emulation)');
      return;
    }

    term.writeln(`Executing: \x1b[36m${cmd}\x1b[0m`);
    term.writeln('\x1b[38;5;244m[sandbox: complete - exit code 0]\x1b[0m');
  };

  const handleClear = () => {
    if (xtermInstance.current) {
      xtermInstance.current.clear();
      xtermInstance.current.write('\x1b[32msafecodium-env$\x1b[0m ');
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#090d16] select-text">
      {/* Terminal Title Bar */}
      <div className="h-7 bg-slate-950 px-3 flex items-center justify-between border-b border-slate-800/80 text-[11px] text-slate-400 select-none">
        <div className="flex items-center space-x-2">
          <TerminalIcon className="w-3.5 h-3.5 text-indigo-400" />
          <span className="font-mono text-slate-300">Terminal (bash / powershell sandbox)</span>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleClear}
            className="hover:text-slate-200 p-1 rounded hover:bg-slate-900 transition-colors"
            title="Clear Terminal"
          >
            <Trash2 className="w-3 h-3" />
          </button>
        </div>
      </div>

      {/* Terminal Canvas */}
      <div ref={terminalRef} className="flex-1 p-2 overflow-hidden" />
    </div>
  );
};

