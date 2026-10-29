const http = require('http');
const { spawn } = require('child_process');

async function inspectChips() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9245',
    '--window-size=1280,800',
    'http://127.0.0.1:5500/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9245/json', res => {
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
  await new Promise(r => setTimeout(r, 1200));

  const res = await send('Runtime.evaluate', {
    expression: `(() => {
      window.activatePathwayMode('academic');
      window.selectAcademicPillar('pqc');
      const strip = document.getElementById('academic-pillars-strip');
      const chips = Array.from(strip.querySelectorAll('.academic-pillar-chip')).map(chip => {
        const cs = window.getComputedStyle(chip);
        const span = chip.querySelector('span:last-child');
        const spanCs = span ? window.getComputedStyle(span) : null;
        return {
          text: chip.innerText.trim(),
          chipWidth: chip.offsetWidth,
          chipScrollWidth: chip.scrollWidth,
          overflow: cs.overflow,
          whiteSpace: cs.whiteSpace,
          maxWidth: cs.maxWidth,
          spanWidth: span ? span.offsetWidth : null,
          spanScrollWidth: span ? span.scrollWidth : null,
          spanOverflow: spanCs ? spanCs.overflow : null,
          spanTextOverflow: spanCs ? spanCs.textOverflow : null
        };
      });
      return {
        stripWidth: strip.offsetWidth,
        stripScrollWidth: strip.scrollWidth,
        chips: chips
      };
    })()`,
    returnByValue: true
  });
  console.log(JSON.stringify(res.result.value, null, 2));

  ws.close();
  edge.kill();
  process.exit(0);
}

inspectChips().catch(err => {
  console.error(err);
  process.exit(1);
});
