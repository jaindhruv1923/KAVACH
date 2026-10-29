const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');

async function capture() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9252',
    '--window-size=1440,900',
    'http://127.0.0.1:5500/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9252/json', res => {
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

  // Improvised mode
  await send('Runtime.evaluate', {
    expression: "window.activatePathwayMode('improvised');"
  });
  await new Promise(r => setTimeout(r, 1000));

  const s = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\view_improvised.png', Buffer.from(s.data, 'base64'));

  console.log('Saved view_improvised.png');
  ws.close();
  edge.kill();
  process.exit(0);
}

capture().catch(err => {
  console.error(err);
  process.exit(1);
});

