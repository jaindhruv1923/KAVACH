/**
 * ==============================================================================
 * KAVACH PORTAL INTEGRATIONS - embedded dashboards inside the main platform
 *
 *   #agents-view      Real AI Agents (autonomous multi-agent cockpit)   /cockpit/
 *   #swarm-view       Live Agent Swarm command center                   /swarm/
 *   #apps-view        Bharat Core Bank A/B comparison portal            /bharat/
 *   #dashboards-view  Directory of every dashboard + embedded viewer
 *
 * URLs come from the shared suite registry (shared_ui/kavach-suite.js) so the
 * same links work on the unified server (port 8001) and on standalone ports.
 * ==============================================================================
 */
(function () {
  'use strict';

  function suiteUrl(key) {
    if (window.KavachSuite) return window.KavachSuite.url(key);
    var fallback = { cockpit: '/cockpit/', swarm: '/swarm/', bharat: '/bharat/', bank: '/bank/', platform: '/' };
    return fallback[key] || '/';
  }
  function dashboards() {
    return (window.KavachSuite && window.KavachSuite.dashboards) || [];
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  var ICON_EXTERNAL = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14L21 3"/></svg>';
  var ICON_RELOAD = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>';

  /* Shared frame used by every embedded dashboard */
  function embedFrame(opts) {
    var src = suiteUrl(opts.key);
    var frameId = opts.viewId + '-frame';
    var facts = (opts.facts || []).map(function (f) { return '<li>' + esc(f) + '</li>'; }).join('');
    return '' +
      '<section class="kv-embed" aria-labelledby="' + opts.viewId + '-title">' +
        '<header class="kv-embed-head">' +
          '<div class="kv-embed-copy">' +
            '<p class="kv-eyebrow">' + esc(opts.eyebrow) + '</p>' +
            '<h2 id="' + opts.viewId + '-title">' + esc(opts.title) + '</h2>' +
            '<p class="kv-embed-lede">' + esc(opts.lede) + '</p>' +
            (facts ? '<ul class="kv-embed-facts">' + facts + '</ul>' : '') +
          '</div>' +
          '<div class="kv-embed-actions">' +
            '<button type="button" class="kv-btn kv-btn-ghost" data-kv-reload="' + frameId + '">' + ICON_RELOAD + '<span>Reload</span></button>' +
            '<a class="kv-btn kv-btn-primary" href="' + esc(src) + '" target="_blank" rel="noopener">' + '<span>Open full screen</span>' + ICON_EXTERNAL + '</a>' +
          '</div>' +
        '</header>' +
        '<div class="kv-embed-frame">' +
          '<iframe id="' + frameId + '" src="' + esc(src) + '" title="' + esc(opts.title) + '" loading="lazy"></iframe>' +
        '</div>' +
        '<p class="kv-embed-note">Served by the main platform at <code>' + esc(src.replace(/^https?:\/\/[^/]+/, '')) + '</code>. If the frame stays empty, start every service with <code>run_all_services.bat</code>.</p>' +
      '</section>';
  }

  function wireReload(root) {
    root.querySelectorAll('[data-kv-reload]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var f = document.getElementById(btn.getAttribute('data-kv-reload'));
        if (f) f.src = f.src.split('?')[0] + '?t=' + Date.now();
      });
    });
  }

  function renderInto(viewId, html) {
    var view = document.getElementById(viewId);
    if (!view) return null;
    if (view.getAttribute('data-kv-rendered') === '1') return view;   // keep iframe state between visits
    view.innerHTML = html;
    view.setAttribute('data-kv-rendered', '1');
    wireReload(view);
    return view;
  }

  window.renderRealAgentsView = function () {
    renderInto('agents-view', embedFrame({
      viewId: 'agents-view', key: 'cockpit',
      eyebrow: 'Real AI Agents',
      title: 'Autonomous multi-agent defense cockpit',
      lede: 'Five specialised agents reason in a bounded ReAct loop, call MCP tools, hand work to each other over A2A and stream every thought, action and observation live.',
      facts: ['19 MCP tools', 'A2A hand-offs', 'Server-sent telemetry', 'Six invariant stages']
    }));
  };

  window.renderLiveSwarmView = function () {
    renderInto('swarm-view', embedFrame({
      viewId: 'swarm-view', key: 'swarm',
      eyebrow: 'Agent Swarm',
      title: 'Live six-sentinel safety swarm',
      lede: 'Run any of the twelve evaluator presets and watch each sentinel gate the payload: intent, AST blast radius, DPDP anonymiser, Graph-of-Thoughts, differential privacy and post-quantum signing.',
      facts: ['12 evaluator presets', 'Step-by-step mode', 'Audit JSON export']
    }));
  };

  window.renderApplicationsWorkView = function () {
    renderInto('apps-view', embedFrame({
      viewId: 'apps-view', key: 'bharat',
      eyebrow: 'Banking Apps',
      title: 'Bharat Core Bank: with and without KAVACH',
      lede: 'The same five banking attacks replayed against a real SQLite ledger, first with a raw autonomous agent and then behind KAVACH, so the difference is measured rather than claimed.',
      facts: ['5 attack scenarios', 'Live treasury ledger', 'Dual-custody escrow']
    }));
  };

  window.renderDashboardsHub = function () {
    var view = document.getElementById('dashboards-view');
    if (!view || view.getAttribute('data-kv-rendered') === '1') return;
    var groups = ['Platform', 'AI Agents', 'Banking', 'Presentation'];
    var list = dashboards();
    var cards = groups.map(function (g) {
      var items = list.filter(function (d) { return d.group === g; }).map(function (d) {
        var href = suiteUrl(d.key);
        return '<article class="kv-hub-card' + (d.primary ? ' is-primary' : '') + '">' +
          '<div><h4>' + esc(d.label) + '</h4><p>' + esc(d.desc) + '</p></div>' +
          '<div class="kv-hub-card-actions">' +
            (d.key === 'platform' ? '' : '<button type="button" class="kv-btn kv-btn-soft" data-kv-preview="' + esc(d.key) + '">Preview here</button>') +
            '<a class="kv-btn kv-btn-link" href="' + esc(href) + '"' + (d.key === 'platform' ? '' : ' target="_blank" rel="noopener"') + '>Open' + (d.key === 'platform' ? '' : ' ' + ICON_EXTERNAL) + '</a>' +
          '</div></article>';
      }).join('');
      return '<div class="kv-hub-group"><h3>' + esc(g) + '</h3><div class="kv-hub-grid">' + items + '</div></div>';
    }).join('');

    view.innerHTML =
      '<section class="kv-hub">' +
        '<header class="kv-hub-head">' +
          '<p class="kv-eyebrow">KAVACH Suite</p>' +
          '<h2>Every dashboard, one website</h2>' +
          '<p class="kv-embed-lede">Pick a dashboard to preview it below without leaving the platform, or open it on its own page. All of them are served by the main platform server.</p>' +
        '</header>' + cards +
        '<section class="kv-embed" id="kv-hub-viewer">' +
          '<header class="kv-embed-head">' +
            '<div class="kv-embed-copy"><p class="kv-eyebrow">Embedded viewer</p><h2 id="kv-hub-viewer-title">Real AI Agents</h2></div>' +
            '<div class="kv-embed-actions">' +
              '<button type="button" class="kv-btn kv-btn-ghost" data-kv-reload="kv-hub-frame">' + ICON_RELOAD + '<span>Reload</span></button>' +
              '<a class="kv-btn kv-btn-primary" id="kv-hub-open" href="' + esc(suiteUrl('cockpit')) + '" target="_blank" rel="noopener"><span>Open full screen</span>' + ICON_EXTERNAL + '</a>' +
            '</div>' +
          '</header>' +
          '<div class="kv-embed-frame"><iframe id="kv-hub-frame" src="about:blank" data-src="' + esc(suiteUrl('cockpit')) + '" title="Dashboard preview" loading="lazy"></iframe></div>' +
        '</section>' +
      '</section>';
    view.setAttribute('data-kv-rendered', '1');
    wireReload(view);

    var frame = document.getElementById('kv-hub-frame');
    frame.src = frame.getAttribute('data-src');
    view.querySelectorAll('[data-kv-preview]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-kv-preview');
        var d = list.filter(function (x) { return x.key === key; })[0];
        frame.src = suiteUrl(key);
        document.getElementById('kv-hub-viewer-title').textContent = d ? d.label : key;
        document.getElementById('kv-hub-open').href = suiteUrl(key);
        document.getElementById('kv-hub-viewer').scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  };

  // Embedded dashboards ask the platform to switch pathway (e.g. their "Back to platform" button)
  window.addEventListener('message', function (event) {
    if (event && event.data && event.data.type === 'KAVACH_NAVIGATE') {
      var pathway = event.data.pathway || 'midsem';
      if (typeof window.activatePathwayMode === 'function') window.activatePathwayMode(pathway);
    }
  });
})();
