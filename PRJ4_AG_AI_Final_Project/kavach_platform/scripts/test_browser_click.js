const http = require('http');
const { spawn } = require('child_process');

async function testHeaderAndViews(port, path) {
  console.log(`\n======================================================`);
  console.log(`TESTING BROWSER ON http://127.0.0.1:${port}${path}`);
  console.log(`======================================================`);

  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const dbgPort = port === 5500 ? 9230 : 9231;
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

  // Check 1: Motion and Particle Canvas removed
  let res = await send('Runtime.evaluate', {
    expression: `(() => {
      const canvas = document.getElementById('interactive-particle-web');
      const motionBtn = document.getElementById('header-motion-btn');
      return {
        particleCanvasPresent: !!canvas,
        motionBtnPresent: !!motionBtn
      };
    })()`,
    returnByValue: true
  });
  console.log('CHECK 1 (Motion & Particle Canvas Removed):', res.result.value);

  // Check 2: Improvised navbar has full text (no ...eplay cut off)
  res = await send('Runtime.evaluate', {
    expression: `(() => {
      window.activatePathwayMode('improvised');
      const switcher = document.getElementById('main-nav-switcher');
      const buttons = Array.from(switcher.querySelectorAll('button')).map(b => b.innerText.trim());
      return {
        pathway: window.CURRENT_PATHWAY,
        centerNavButtons: buttons,
        buttonCount: buttons.length
      };
    })()`,
    returnByValue: true
  });
  console.log('CHECK 2 (Improvised Nav Buttons & Spacing):', res.result.value);

  // Check 3: Click Academic Weapon Button
  res = await send('Runtime.evaluate', {
    expression: `(() => {
      const btn = document.getElementById('pathway-btn-academic');
      if (btn) btn.click();
      const view = document.getElementById('academic-view');
      const strip = document.getElementById('academic-pillars-strip');
      const ws = document.getElementById('academic-pillar-workspace');
      const chips = Array.from(strip ? strip.querySelectorAll('.academic-pillar-chip') : []).map(c => c.innerText.trim().replace(/\\s+/g, ' '));
      return {
        tabActive: btn && btn.classList.contains('active'),
        academicViewDisplay: view ? view.style.display : null,
        currentPathway: window.CURRENT_PATHWAY,
        pillarChipsCount: chips.length,
        pillarChipsSample: chips.slice(0, 4),
        workspaceHasMath: !!(ws && ws.querySelector('#academic-math-container')),
        workspaceHasSim: !!(ws && ws.querySelector('#academic-flow-sim'))
      };
    })()`,
    returnByValue: true
  });
  console.log('CHECK 3 (Academic Weapon 10 Frontiers Cockpit):', res.result.value);

  ws.close();
  edge.kill();
}

async function main() {
  await testHeaderAndViews(5500, '/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html');
  await testHeaderAndViews(5502, '/KAVACH-main/01_KAVACH_Platform/frontend/index.html');
  process.exit(0);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
