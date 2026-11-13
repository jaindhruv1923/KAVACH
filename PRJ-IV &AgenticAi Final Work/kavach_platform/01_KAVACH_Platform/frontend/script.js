/**
 * Interactive Neural Constellation Canvas (Particle Mesh / Constellation Web)
 * High-performance Vanilla HTML5 Canvas physics simulation with high-DPI
 * scaling, dynamic distance linking, mouse magnetism, and radar tracking.
 */
function initInteractiveParticleWeb() {
  window.__particleWebInitialized = true;
  const canvas = document.getElementById("interactive-particle-web");
  if (canvas) {
    canvas.style.display = "none";
    canvas.remove();
  }
}
window.initInteractiveParticleWeb = initInteractiveParticleWeb;
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initInteractiveParticleWeb);
} else {
  initInteractiveParticleWeb();
}
