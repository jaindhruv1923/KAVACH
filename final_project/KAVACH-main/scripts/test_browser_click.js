const http = require('http');
const { spawn } = require('child_process');

async function testPort(port, path) {
  console.log(`\n========================================`);
  console.log(`TESTING http://127.0.0.1:${port}${path}`);
  console.log(`========================================`);

  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const dbgPort = port === 5500 ? 9225 : 9226;
  const edge = spawn(edgePath, [
    '--headless=new',
    `--remote-debugging-port=${dbgPort}`,
    '--disable-gpu',
    `http://127.0.0.1:${port}${path}`
  ]);

  await new Promise(r => setTimeout(r, 2500));

  const json = await new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${dbgPort}/json`, res => {
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
  await send('Page.enable');
  await new Promise(r => setTimeout(r, 1200));

  // Test 1: Click #pathway-btn-academic
  let res = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById('pathway-btn-academic');
      if (btn) btn.click();
      const view = document.getElementById('academic-view');
      const headerBtn = document.getElementById('header-academic-btn');
      const strip = document.getElementById('academic-pillars-strip');
      return {
        clickedTab: !!btn,
        tabActive: btn && btn.classList.contains('active'),
        headerBtnActive: headerBtn && headerBtn.classList.contains('active'),
        viewDisplay: view ? view.style.display : null,
        stripChips: strip ? strip.children.length : 0
      };
    })()`,
    returnByValue: true
  });
  console.log('CLICK #pathway-btn-academic RESULT:', res.result.value);

  // Switch back to midsem
  await send('Runtime.evaluate', {
    expression: `window.activatePathwayMode('midsem')`
  });

  // Test 2: Click #header-academic-btn
  res = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById('header-academic-btn');
      if (btn) btn.click();
      const tabBtn = document.getElementById('pathway-btn-academic');
      const view = document.getElementById('academic-view');
      const strip = document.getElementById('academic-pillars-strip');
      return {
        clickedHeaderBtn: !!btn,
        headerBtnActive: btn && btn.classList.contains('active'),
        tabActive: tabBtn && tabBtn.classList.contains('active'),
        viewDisplay: view ? view.style.display : null,
        stripChips: strip ? strip.children.length : 0
      };
    })()`,
    returnByValue: true
  });
  console.log('CLICK #header-academic-btn RESULT:', res.result.value);

  ws.close();
  edge.kill();
}

async function main() {
  await testPort(5500, '/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html');
  await testPort(5502, '/KAVACH-main/01_KAVACH_Platform/frontend/index.html');
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
