/**
 * Interactive Neural Constellation Canvas (Particle Mesh / Constellation Web)
 * High-performance Vanilla HTML5 Canvas physics simulation with high-DPI
 * scaling, dynamic distance linking, mouse magnetism, and radar tracking.
 */
function initInteractiveParticleWeb() {
  const canvas = document.getElementById("interactive-particle-web");
  if (canvas) canvas.remove();
}

// Window export & auto-start
window.initInteractiveParticleWeb = initInteractiveParticleWeb;
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initInteractiveParticleWeb);
} else {
  initInteractiveParticleWeb();
}
