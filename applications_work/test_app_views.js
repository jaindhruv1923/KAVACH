const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');

async function testAppViews() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9265',
    '--window-size=1560,1050',
    'http://127.0.0.1:5500/applications_work/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9265/json', res => {
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

  // 1. In Phase 1 (Without KAVACH): select Scenario 2 (CEO jailbreak) and dispatch
  await send('Runtime.evaluate', {
    expression: "window.setPhase(1); window.selectScenario('ceo_jailbreak'); window.dispatchTransaction();"
  });
  await new Promise(r => setTimeout(r, 2000));

  const s1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\app_phase1_without_kavach.png', Buffer.from(s1.data, 'base64'));
  console.log('Saved app_phase1_without_kavach.png');

  // 2. Switch to Phase 3 (With KAVACH) and dispatch Scenario 2 again
  await send('Runtime.evaluate', {
    expression: "window.resetBankLedger(); window.setPhase(3); window.selectScenario('ceo_jailbreak'); window.dispatchTransaction();"
  });
  await new Promise(r => setTimeout(r, 2000));

  const s2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\jaind\\.gemini\\antigravity\\brain\\f9edf30a-d672-440d-896a-69ec3ccbc3bf\\app_phase3_with_kavach.png', Buffer.from(s2.data, 'base64'));
  console.log('Saved app_phase3_with_kavach.png');

  ws.close();
  edge.kill();
  process.exit(0);
}

testAppViews().catch(err => {
  console.error(err);
  process.exit(1);
});

