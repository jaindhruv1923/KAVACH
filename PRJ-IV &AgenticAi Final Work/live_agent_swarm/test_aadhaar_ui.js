const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');

async function testAadhaarBlock() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9260',
    '--window-size=1560,1050',
    'http://127.0.0.1:5500/live_agent_dashboard/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9260/json', res => {
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

  // Load Aadhaar leak preset
  await send('Runtime.evaluate', {
    expression: "window.loadPreset('aadhaar_leak'); document.getElementById('btn-run-swarm').click();"
  });

  // Wait for swarm execution
  await new Promise(r => setTimeout(r, 3200));

  // Capture screenshot of blocked Aadhaar leak
  const s = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\dashboard_aadhaar_blocked.png', Buffer.from(s.data, 'base64'));
  console.log('Saved dashboard_aadhaar_blocked.png!');

  // Check DOM values
  const verdict = await send('Runtime.evaluate', {
    expression: "document.getElementById('metric-verdict').innerText"
  });
  const threats = await send('Runtime.evaluate', {
    expression: "document.getElementById('metric-threats').innerText"
  });
  console.log('DOM Verdict:', verdict.result.value);
  console.log('DOM Threats:', threats.result.value);

  ws.close();
  edge.kill();
  process.exit(0);
}

testAadhaarBlock().catch(err => {
  console.error(err);
  process.exit(1);
});

