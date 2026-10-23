/**
 * Particle mesh web disabled per user request.
 */
function initInteractiveParticleWeb() {
  const canvas = document.getElementById("interactive-particle-web");
  if (canvas && canvas.parentNode) {
    canvas.parentNode.removeChild(canvas);
  }
}

// Window export & auto-start
window.initInteractiveParticleWeb = initInteractiveParticleWeb;
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initInteractiveParticleWeb);
} else {
  initInteractiveParticleWeb();
}
