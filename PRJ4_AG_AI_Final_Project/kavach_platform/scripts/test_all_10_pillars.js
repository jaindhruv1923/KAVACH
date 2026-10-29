const http = require('http');
const { spawn } = require('child_process');

async function testAllChips() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9250',
    '--window-size=1440,900',
    'http://127.0.0.1:5500/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2000));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9250/json', res => {
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

  await send('Runtime.enable');
  await new Promise(r => setTimeout(r, 1000));

  const evalCode = `
    (function() {
      window.activatePathwayMode('academic');
      var pillars = ['dp', 'got', 'watermark', 'lattice', 'pqc', 'wallet', 'entailment', 'saga', 'causal', 'ablation'];
      var results = [];
      for (var i = 0; i < pillars.length; i++) {
        var pid = pillars[i];
        window.selectAcademicPillar(pid);
        var activeChip = document.querySelector('.academic-pillar-chip.active');
        var workspaceTitle = document.querySelector('#academic-pillar-workspace h3');
        var chipBg = activeChip ? window.getComputedStyle(activeChip).backgroundImage || window.getComputedStyle(activeChip).backgroundColor : null;
        var chipColor = activeChip ? window.getComputedStyle(activeChip).color : null;
        results.push({
          pillar: pid,
          chipText: activeChip ? activeChip.innerText.trim().replace(/\\s+/g, ' ') : null,
          title: workspaceTitle ? workspaceTitle.innerText.trim() : null,
          chipColor: chipColor,
          chipBg: chipBg
        });
      }
      return results;
    })()
  `;

  const res = await send('Runtime.evaluate', {
    expression: evalCode,
    returnByValue: true
  });

  console.log('Results:');
  console.log(JSON.stringify(res.result.value, null, 2));

  ws.close();
  edge.kill();
  process.exit(0);
}

testAllChips().catch(e => {
  console.error(e);
  process.exit(1);
});
