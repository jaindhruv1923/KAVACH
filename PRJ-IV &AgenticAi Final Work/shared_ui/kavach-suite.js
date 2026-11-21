/**
 * KAVACH SUITE NAVIGATION
 * ---------------------------------------------------------------------------
 * One registry of every KAVACH dashboard + a slim top bar rendered on each of
 * them, so the whole project behaves like a single website.
 *
 * Usage (in any dashboard <head> or before </body>):
 *   <link rel="stylesheet" href="/suite/kavach-suite.css">
 *   <script src="/suite/kavach-suite.js" data-page="cockpit" defer></script>
 *
 * data-page      key of the current dashboard (see DASHBOARDS below)
 * data-placement "header" -> render inside the page's fixed .app-header
 *                "top"    -> render as the first element of <body> (default)
 *
 * URL resolution
 *   - Served by the main platform (port 8001 or any production host): every
 *     dashboard is a path on the same origin (/cockpit/, /bharat/, ...).
 *   - Opened from a standalone service port (8000, 8002, 8003, 8050): links
 *     point back to the main platform on port 8001 of the same host.
 */
(function () {
  'use strict';
  if (window.KavachSuite) return;

  var script = document.currentScript || document.querySelector('script[src*="kavach-suite.js"]');
  var PAGE = (script && script.getAttribute('data-page')) || '';
  var PLACEMENT = (script && script.getAttribute('data-placement')) || 'top';

  var STANDALONE_PORTS = { '8000': 1, '8002': 1, '8003': 1, '8005': 1, '8050': 1 };
  var loc = window.location;
  var isGhPages = loc.hostname.indexOf('github.io') !== -1;
  var ghPrefix = (isGhPages && loc.pathname.split('/')[1]) ? '/' + loc.pathname.split('/')[1] : '';
  var PLATFORM_ORIGIN = loc.protocol === 'file:'
    ? 'http://127.0.0.1:8001'
    : (STANDALONE_PORTS[loc.port] ? loc.protocol + '//' + loc.hostname + ':8001' : (loc.origin + ghPrefix));

  var DASHBOARDS = [
    { key: 'platform',  group: 'Platform',     label: 'Platform Home',          path: '/',          desc: 'Overview, architecture flowchart, verification suite and research views.' },
    { key: 'console',   group: 'Platform',     label: 'Live Console',           path: '/console',   desc: 'Incident workspace: run requests through every security gate.' },
    { key: 'midsem',    group: 'Platform',     label: 'Mid-Sem Foundation',     path: '/midsem',    desc: 'The v1.0 baseline: 8-stage deterministic pipeline.' },
    { key: 'evolution', group: 'Platform',     label: 'Post-Mid-Sem Evolution', path: '/evolution', desc: 'Ten documented limitations and how each was solved.' },
    { key: 'cockpit',   group: 'AI Agents',    label: 'Real AI Agents',         path: '/cockpit/',  desc: 'Autonomous multi-agent cockpit: ReAct loop, MCP tools, A2A, live telemetry.', primary: true },
    { key: 'swarm',     group: 'AI Agents',    label: 'Live Agent Swarm',       path: '/swarm/',    desc: 'Six-sentinel safety swarm with twelve evaluator presets.' },
    { key: 'bharat',    group: 'Banking',      label: 'Bharat Core Bank',       path: '/bharat/',   desc: 'A/B simulation: the same attacks with and without KAVACH.' },
    { key: 'bank',      group: 'Banking',      label: 'Banking Highway',        path: '/bank/',     desc: 'Governed payment console, HITL desk, SAGA and Merkle audit.' },
    { key: 'guide',     group: 'Presentation', label: 'Stakeholder Guide',      path: '/guide',     desc: 'The system explained for customer, DevOps, auditor and CISO.' },
    { key: 'motion',    group: 'Presentation', label: 'Motion Studio',          path: '/motion/',   desc: 'Animated diagrams used in the presentation.' },
    { key: 'report',    group: 'Presentation', label: 'Mid-Sem Report',         path: '/reports/KAVACH_MidSem_Comprehensive_Submission_Report.html', desc: 'Comprehensive mid-semester submission report.' },
    { key: 'matrix',    group: 'Presentation', label: 'Coverage Matrix',        path: '/reports/KAVACH_Midsem_1_Slide_Coverage_Matrix.html', desc: 'One-slide rubric coverage matrix.' }
  ];
  var QUICK = ['cockpit', 'swarm', 'bharat', 'bank', 'console'];
  var GROUPS = ['Platform', 'AI Agents', 'Banking', 'Presentation'];

  function find(key) {
    for (var i = 0; i < DASHBOARDS.length; i++) if (DASHBOARDS[i].key === key) return DASHBOARDS[i];
    return null;
  }
  function url(key) {
    var d = find(key);
    return d ? PLATFORM_ORIGIN + d.path : PLATFORM_ORIGIN + '/';
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var ICONS = {
    game: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2"/><path d="M6 12h4m-2-2v4m10-2h.01m-3 0h.01"/></svg>',
    shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    grid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>',
    chevron: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
    code: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    flow: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><path d="M6 9v3a3 3 0 0 0 3 3h6"/></svg>',
    sigma: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 4H6l6 8-6 8h12"/></svg>',
    chat: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    scale: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18M5 21h14M3 7h18M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/></svg>'
  };

  /* Story Mode Lazy-Loader Fallback */
  if (typeof window.openKavachStoryMode !== 'function') {
    window.openKavachStoryMode = function (ch) {
      if (document.getElementById('kavach-story-script')) {
        setTimeout(function () {
          if (typeof window.openKavachStoryMode === 'function') window.openKavachStoryMode(ch);
        }, 50);
        return;
      }
      var s = document.createElement('script');
      s.id = 'kavach-story-script';
      var fallbackPath = window.location.pathname.includes('/cockpit') || window.location.pathname.includes('/kavach_agent_core') ? '../suite/kavach-story-mode.js?v=2.4' : 'suite/kavach-story-mode.js?v=2.4';
      s.src = PLATFORM_ORIGIN + '/suite/kavach-story-mode.js?v=2.4';
      s.onerror = function() {
        this.onerror = null;
        this.src = fallbackPath;
      };
      s.onload = function () {
        if (typeof window.openKavachStoryMode === 'function') window.openKavachStoryMode(ch);
      };
      document.body.appendChild(s);
    };
  }

  /* Tools shown at the top-right when the current page provides them */
  var TOOLS = [
    { id: 'ide',   label: 'Inbuilt IDE',         short: 'IDE',   icon: 'code',  fn: 'openCodebaseIdeModal' },
    { id: 'flow',  label: 'Implementation Flow', short: 'Flow',  icon: 'flow',  fn: 'openImplementationModal', arg: 'journey' },
    { id: 'math',  label: 'Math Guide',          short: 'Math',  icon: 'sigma', fn: 'openEli5AcademicModal' },
    { id: 'rules', label: 'Rules Codex',         short: 'Rules', icon: 'scale', fn: 'openGovRulesModal', onlyOn: ['bank'] },
    { id: 'ask',   label: 'Ask AI',              short: 'Ask',   icon: 'chat',  fn: 'toggleChatbot' }
  ];

  function buildBar() {
    var current = find(PAGE);
    var bar = document.createElement('nav');
    bar.className = 'kv-suite';
    bar.id = 'kv-suite';
    if (PAGE === 'platform') bar.classList.add('kv-suite--platform');   // the platform has its own section tabs
    bar.setAttribute('aria-label', 'KAVACH dashboards');

    var quick = QUICK.map(function (k) {
      var d = find(k);
      var cls = 'kv-link' + (d.primary ? ' kv-link-primary' : '') + (k === PAGE ? ' is-current' : '') + (k === 'console' || k === 'bank' ? ' kv-optional' : '');
      return '<a class="' + cls + '" href="' + esc(url(k)) + '"' + (k === PAGE ? ' aria-current="page"' : '') + '>' +
        (d.primary ? '<span class="kv-live-dot" aria-hidden="true"></span>' : '') + esc(d.label) + '</a>';
    }).join('');

    var groups = GROUPS.map(function (g) {
      var items = DASHBOARDS.filter(function (d) { return d.group === g; }).map(function (d) {
        return '<a class="kv-mega-item' + (d.key === PAGE ? ' is-current' : '') + '" href="' + esc(url(d.key)) + '">' +
          '<strong>' + esc(d.label) + (d.key === PAGE ? ' <em>you are here</em>' : '') + '</strong><span>' + esc(d.desc) + '</span></a>';
      }).join('');
      return '<div class="kv-mega-group"><h4>' + esc(g) + '</h4>' + items + '</div>';
    }).join('');

    bar.innerHTML =
      '<div class="kv-suite-inner">' +
        '<div class="kv-suite-left">' +
          '<a class="kv-brand" href="' + esc(url('platform')) + '" title="KAVACH platform home">' + ICONS.shield +
            '<span>KAVACH</span><small>' + esc(current ? current.label : 'Suite') + '</small></a>' +
          '<span class="kv-quick">' + quick + '</span>' +
          '<button type="button" class="kv-menu-trigger" aria-expanded="false" aria-controls="kv-mega">' + ICONS.grid +
            '<span>All dashboards</span>' + ICONS.chevron + '</button>' +
        '</div>' +
        '<div class="kv-suite-right" id="kv-suite-tools"></div>' +
      '</div>' +
      '<div class="kv-mega" id="kv-mega" role="region" aria-label="All KAVACH dashboards">' +
        '<div class="kv-mega-inner">' + groups +
          '<div class="kv-mega-foot"><span>Every dashboard runs from the main platform server.</span>' +
          '<code>run_all_services.bat</code></div>' +
        '</div>' +
      '</div>';
    return bar;
  }

  function renderTools(bar) {
    var box = bar.querySelector('#kv-suite-tools');
    if (!box) return;
    var html = [];
    TOOLS.forEach(function (t) {
      if (t.onlyOn && t.onlyOn.indexOf(PAGE) === -1) return;
      if (typeof window[t.fn] !== 'function') return;
      if (html.length) html.push('<span class="kv-sep" aria-hidden="true"></span>');
      html.push('<button type="button" class="kv-tool" data-kv-tool="' + t.id + '" title="' + esc(t.label) + '">' +
        ICONS[t.icon] + '<span class="kv-tool-label">' + esc(t.label) + '</span><span class="kv-tool-label-short">' + esc(t.short) + '</span></button>');
    });
    box.innerHTML = html.join('');
    box.querySelectorAll('[data-kv-tool]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var t = TOOLS.filter(function (x) { return x.id === btn.getAttribute('data-kv-tool'); })[0];
        var fn = t && window[t.fn];
        if (typeof fn === 'function') {
          closeMega(bar);
          t.arg ? fn(t.arg) : fn();
        }
      });
    });
    document.documentElement.classList.toggle('kv-has-tools', html.length > 0);
  }

  function closeMega(bar) {
    bar.classList.remove('is-open');
    var trig = bar.querySelector('.kv-menu-trigger');
    if (trig) trig.setAttribute('aria-expanded', 'false');
  }

  function wireMega(bar) {
    var trig = bar.querySelector('.kv-menu-trigger');
    var hoverTimer = null;
    function open() {
      bar.classList.add('is-open');
      trig.setAttribute('aria-expanded', 'true');
    }
    trig.addEventListener('click', function (e) {
      e.stopPropagation();
      bar.classList.contains('is-open') ? closeMega(bar) : open();
    });
    if (window.matchMedia && window.matchMedia('(hover: hover)').matches) {
      trig.addEventListener('mouseenter', function () { clearTimeout(hoverTimer); hoverTimer = setTimeout(open, 120); });
      bar.addEventListener('mouseleave', function () { clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { closeMega(bar); }, 220); });
      bar.querySelector('.kv-mega').addEventListener('mouseenter', function () { clearTimeout(hoverTimer); });
    }
    document.addEventListener('click', function (e) { if (!bar.contains(e.target)) closeMega(bar); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMega(bar); });
  }

  /* Keep body offset in sync with a fixed .app-header that now contains the bar */
  function syncFixedHeader(header) {
    function apply() {
      var h = header.getBoundingClientRect().height;
      document.documentElement.style.setProperty('--kv-header-h', Math.round(h) + 'px');
    }
    apply();
    if (window.ResizeObserver) new ResizeObserver(apply).observe(header);
    window.addEventListener('resize', apply);
  }

  /* Any <a data-kv-link="swarm"> on a dashboard points at the right address for this deployment */
  function resolveLinks() {
    document.querySelectorAll('a[data-kv-link]').forEach(function (a) {
      if (find(a.getAttribute('data-kv-link'))) a.href = url(a.getAttribute('data-kv-link'));
    });
  }

  function mount() {
    resolveLinks();
    if (window.self !== window.top) {
      document.documentElement.classList.add('kv-embedded');
      return;
    }
    if (document.getElementById('kv-suite')) return;
    var bar = buildBar();
    var header = PLACEMENT === 'header' ? document.querySelector('.app-header') : null;
    if (header) {
      header.insertBefore(bar, header.firstChild);
      document.documentElement.classList.add('kv-header-mode');
      syncFixedHeader(header);
    } else {
      document.body.insertBefore(bar, document.body.firstChild);
      document.documentElement.classList.add('kv-top-mode');
    }
    wireMega(bar);
    renderTools(bar);
    // Some dashboards register their tools late; re-check once everything has loaded.
    window.addEventListener('load', function () { renderTools(bar); setTimeout(function () { renderTools(bar); }, 600); });
  }

  window.KavachSuite = { url: url, dashboards: DASHBOARDS, page: PAGE, platformOrigin: PLATFORM_ORIGIN };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})();
