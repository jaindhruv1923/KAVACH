const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');

async function testDashboard() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9255',
    '--window-size=1560,1050',
    'http://127.0.0.1:5500/live_agent_dashboard/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9255/json', res => {
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

  // Initial loaded screenshot
  const s1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\dashboard_initial.png', Buffer.from(s1.data, 'base64'));
  console.log('Saved dashboard_initial.png');

  // Click Execute Swarm
  await send('Runtime.evaluate', {
    expression: "document.getElementById('btn-run-swarm').click();"
  });

  // Wait for swarm to finish (approx 3 seconds)
  await new Promise(r => setTimeout(r, 3200));

  // Capture executed state
  const s2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\dashboard_executed.png', Buffer.from(s2.data, 'base64'));
  console.log('Saved dashboard_executed.png');

  // Test an attack preset (Preset 2: Jailbreak)
  await send('Runtime.evaluate', {
    expression: "window.loadPreset('jailbreak'); document.getElementById('btn-run-swarm').click();"
  });
  await new Promise(r => setTimeout(r, 3200));

  const s3 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\dashboard_jailbreak_blocked.png', Buffer.from(s3.data, 'base64'));
  console.log('Saved dashboard_jailbreak_blocked.png');

  ws.close();
  edge.kill();
  process.exit(0);
}

testDashboard().catch(err => {
  console.error(err);
  process.exit(1);
});
