const { contextBridge, ipcRenderer } = require('electron');

// Expose safe, isolated APIs to the frontend React window object
contextBridge.exposeInMainWorld('safecodiumDesktop', {
  isDesktop: true,
  openDirectory: () => ipcRenderer.invoke('dialog:openDirectory'),
  readFile: (filePath) => ipcRenderer.invoke('fs:readFile', filePath),
  saveFile: (filePath, content) => ipcRenderer.invoke('fs:saveFile', { filePath, content }),
});

