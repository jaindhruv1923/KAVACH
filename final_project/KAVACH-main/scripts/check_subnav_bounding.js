const http = require('http');
const { spawn } = require('child_process');

async function checkNoClipping() {
  const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
  const edge = spawn(edgePath, [
    '--headless=new',
    '--remote-debugging-port=9240',
    '--window-size=1280,800',
    'http://127.0.0.1:5500/final_project/KAVACH-main/01_KAVACH_Platform/frontend/index.html'
  ]);

  await new Promise(r => setTimeout(r, 2200));

  const json = await new Promise((resolve, reject) => {
    http.get('http://127.0.0.1:9240/json', res => {
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

  for (const pathway of ['midsem', 'improvised', 'academic']) {
    const res = await send('Runtime.evaluate', {
      expression: `(() => {
        window.activatePathwayMode('${pathway}');
        const subnav = document.getElementById('app-header-subnav');
        const switcher = document.getElementById('main-nav-switcher');
        const subRect = subnav.getBoundingClientRect();
        const btns = Array.from(switcher.querySelectorAll('button')).map(b => {
          const r = b.getBoundingClientRect();
          return {
            text: b.innerText.trim(),
            width: Math.round(r.width),
            left: Math.round(r.left),
            right: Math.round(r.right),
            isWithinSubnav: r.left >= subRect.left - 2 && r.right <= subRect.right + 2
          };
        });
        return {
          pathway: '${pathway}',
          subnavWidth: Math.round(subRect.width),
          buttonsCount: btns.length,
          allWithinBounds: btns.every(b => b.isWithinSubnav),
          buttons: btns
        };
      })()`,
      returnByValue: true
    });
    console.log(JSON.stringify(res.result.value, null, 2));
  }

  ws.close();
  edge.kill();
  process.exit(0);
}

checkNoClipping().catch(err => {
  console.error(err);
  process.exit(1);
});
