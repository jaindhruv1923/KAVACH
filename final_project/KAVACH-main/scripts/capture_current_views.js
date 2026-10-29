const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');

async function capture() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9247',
    '--window-size=1440,900',
    'http://127.0.0.1:5500/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9247/json', res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });

  const page = json.find(t => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);

  let id = 1;
  function send(method, params = {}) {
    return new Promise((resolve) => {
      const msgId = id++;
      const handler = (event) => {
        const res = JSON.parse(event.data);
        if (res.id === msgId) {
          ws.removeEventListener('message', handler);
          resolve(res.result);
        }
      };
      ws.addEventListener('message', handler);
      ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  await send('Page.enable');
  await send('Runtime.enable');
  await new Promise(r => setTimeout(r, 1000));

  // Snapshot 1: Default Improvised v3.0 mode
  const s1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\view1_default.png', Buffer.from(s1.data, 'base64'));

  // Switch to Academic Weapon
  await send('Runtime.evaluate', {
    expression: "document.getElementById('pathway-btn-academic').click();"
  });
  await new Promise(r => setTimeout(r, 1000));

  // Snapshot 2: Academic Weapon Cockpit with 10 Frontier buttons
  const s2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\view2_academic.png', Buffer.from(s2.data, 'base64'));

  console.log('Successfully captured view1_default.png and view2_academic.png');
  ws.close();
  edge.kill();
  process.exit(0);
}

capture().catch(err => {
  console.error(err);
  process.exit(1);
});
