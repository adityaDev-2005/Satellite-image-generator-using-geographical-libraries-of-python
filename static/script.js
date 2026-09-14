const form = document.getElementById("query-form");
const input = document.getElementById("query-input");
const analyzeButton = document.getElementById("analyze-button");
const heroCta = document.getElementById("hero-cta");
const querySection = document.getElementById("query-section");
const statusPanel = document.getElementById("status-panel");
const statusSteps = document.querySelectorAll("#status-steps li");
const errorPanel = document.getElementById("error-panel");
const errorMessage = document.getElementById("error-message");
const results = document.getElementById("results");
const newAnalysisButton = document.getElementById("new-analysis-button");
const exampleChips = document.querySelectorAll(".example-chip");

let statusTimer = null;
let map = null;
let mapAoiLayer = null;
let mapMarker = null;
let isSubmitting = false;

function hideAll() {
  statusPanel.classList.add("hidden");
  errorPanel.classList.add("hidden");
  results.classList.add("hidden");
}

function startStatusAnimation() {
  clearInterval(statusTimer);
  statusSteps.forEach((step) => step.classList.remove("active", "done"));
  statusPanel.classList.remove("hidden");

  let current = 0;
  statusSteps[0]?.classList.add("active");

  statusTimer = setInterval(() => {
    if (current < statusSteps.length - 1) {
      statusSteps[current].classList.remove("active");
      statusSteps[current].classList.add("done");
      current += 1;
      statusSteps[current].classList.add("active");
    }
  }, 1500);
}

function stopStatusAnimation() {
  clearInterval(statusTimer);
  statusTimer = null;
  statusPanel.classList.add("hidden");
}

function setSubmitting(submitting) {
  isSubmitting = submitting;
  analyzeButton.disabled = submitting;
  analyzeButton.classList.toggle("loading", submitting);
  exampleChips.forEach((chip) => { chip.disabled = submitting; });
}

function showError(message) {
  errorMessage.textContent = message;
  errorPanel.classList.remove("hidden");
  errorPanel.scrollIntoView({ behavior: "smooth", block: "center" });
}

function formatAoi(aoi) {
  const round = (n) => Number(n).toFixed(4);
  return `${round(aoi.west)}, ${round(aoi.south)}, ${round(aoi.east)}, ${round(aoi.north)}`;
}

function formatDateShort(isoString) {
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return isoString;
  return date.toLocaleDateString(undefined, { day: "2-digit", month: "short", year: "numeric" });
}

function formatDateLong(isoString) {
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return isoString;
  return date.toLocaleString(undefined, {
    year: "numeric", month: "short", day: "numeric",
    hour: "2-digit", minute: "2-digit"
  });
}

function interpretNdvi(meanNdvi) {
  if (!Number.isFinite(meanNdvi)) {
    return {
      label: "Unavailable",
      summary: "A vegetation assessment could not be determined from the available NDVI statistics."
    };
  }

  if (meanNdvi < 0) {
    return {
      label: "Very low",
      summary: "The area shows a very low vegetation signal overall, with the mean NDVI below zero."
    };
  }

  if (meanNdvi < 0.2) {
    return {
      label: "Low",
      summary: "The area shows a low vegetation signal overall, with the mean NDVI close to the lower end of the vegetation range."
    };
  }

  if (meanNdvi < 0.4) {
    return {
      label: "Moderate",
      summary: "The area shows a moderate vegetation signal overall. The AOI likely contains a mixture of vegetation and less-vegetated surfaces."
    };
  }

  if (meanNdvi < 0.6) {
    return {
      label: "Strong",
      summary: "The area shows a strong vegetation signal overall, with the mean NDVI indicating substantial vegetation response."
    };
  }

  return {
    label: "Very strong",
    summary: "The area shows a very strong vegetation signal overall, with a high mean NDVI."
  };
}

function primaryPlaceName(location, address) {
  if (address) {
    const firstPart = address.split(",")[0].trim();
    if (firstPart) return firstPart;
  }
  return location;
}

function renderResults(data) {
  const placeName = primaryPlaceName(data.location, data.address);
  const coordinates = `${Number(data.latitude).toFixed(4)}, ${Number(data.longitude).toFixed(4)}`;

  document.getElementById("res-title").textContent = placeName;
  document.getElementById("res-subline").textContent =
    `Sentinel-2 L2A · ${formatDateShort(data.acquisition_date)} · ${Number(data.cloud_cover).toFixed(1)}% cloud cover`;

  document.getElementById("overview-date").textContent = formatDateLong(data.acquisition_date);
  document.getElementById("overview-cloud").textContent = `${Number(data.cloud_cover).toFixed(1)}%`;
  document.getElementById("overview-scene").textContent = data.scene_id;
  document.getElementById("overview-location").textContent = placeName;
  document.getElementById("overview-coordinates").textContent = coordinates;
  document.getElementById("overview-address").textContent = data.address;

  document.getElementById("res-location").textContent = data.location;
  document.getElementById("res-address").textContent = data.address;
  document.getElementById("res-lat").textContent = Number(data.latitude).toFixed(5);
  document.getElementById("res-lon").textContent = Number(data.longitude).toFixed(5);
  document.getElementById("res-aoi").textContent = formatAoi(data.aoi);
  document.getElementById("res-scene").textContent = data.scene_id;
  document.getElementById("res-date").textContent = formatDateLong(data.acquisition_date);
  document.getElementById("res-cloud").textContent = `${Number(data.cloud_cover).toFixed(1)}%`;

  const ndviMean = Number(data.ndvi_statistics.mean);
  document.getElementById("stat-min").textContent = Number(data.ndvi_statistics.min).toFixed(3);
  document.getElementById("stat-mean").textContent = ndviMean.toFixed(3);
  document.getElementById("stat-max").textContent = Number(data.ndvi_statistics.max).toFixed(3);

  const assessment = interpretNdvi(ndviMean);
  document.getElementById("assessment-title").textContent = `${assessment.label} vegetation signal`;
  document.getElementById("assessment-badge").textContent = `Mean NDVI ${ndviMean.toFixed(3)}`;
  document.getElementById("assessment-summary").textContent = assessment.summary;

  document.getElementById("rgb-image").src = data.rgb_image;
  document.getElementById("ndvi-image").src = data.ndvi_image;

  renderMap(data);
  results.classList.remove("hidden");
  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderMap(data) {
  const bounds = [[data.aoi.south, data.aoi.west], [data.aoi.north, data.aoi.east]];

  if (!map) {
    map = L.map("map", { attributionControl: true, zoomControl: true });
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);
  }

  if (mapAoiLayer) map.removeLayer(mapAoiLayer);
  if (mapMarker) map.removeLayer(mapMarker);

  mapAoiLayer = L.rectangle(bounds, {
    color: "#20c7b0", weight: 2, fillColor: "#20c7b0", fillOpacity: 0.08
  }).addTo(map);

  mapMarker = L.circleMarker([data.latitude, data.longitude], {
    radius: 5, color: "#d9aa4d", fillColor: "#d9aa4d", fillOpacity: 1, weight: 1
  }).addTo(map);

  map.fitBounds(bounds, { padding: [24, 24] });
  setTimeout(() => map.invalidateSize(), 80);
}

async function runAnalysis(query) {
  if (isSubmitting) return;

  hideAll();
  startStatusAnimation();
  setSubmitting(true);

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    let data;
    try {
      data = await response.json();
    } catch {
      throw new Error("The server returned an invalid response.");
    }

    if (!data.success) {
      showError(data.error || "The request could not be completed.");
      return;
    }

    renderResults(data);
  } catch (err) {
    console.error(err);
    showError(err.message || "Could not reach the server. Please try again.");
  } finally {
    stopStatusAnimation();
    setSubmitting(false);
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const query = input.value.trim();
  if (query) runAnalysis(query);
});

exampleChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    if (isSubmitting) return;
    input.value = chip.textContent.trim();
    runAnalysis(input.value);
  });
});

heroCta.addEventListener("click", () => {
  querySection.scrollIntoView({ behavior: "smooth", block: "start" });
  setTimeout(() => input.focus(), 350);
});

newAnalysisButton.addEventListener("click", () => {
  hideAll();
  input.value = "";
  querySection.scrollIntoView({ behavior: "smooth", block: "start" });
  setTimeout(() => input.focus(), 350);
});

/* Image viewer */
const viewerOverlay = document.getElementById("viewer-overlay");
const viewerImage = document.getElementById("viewer-image");
const viewerTitle = document.getElementById("viewer-title");
const viewerStage = document.getElementById("viewer-stage");
let viewerScale = 1;
let viewerOffsetX = 0;
let viewerOffsetY = 0;
let isPanning = false;
let panStartX = 0;
let panStartY = 0;
let currentDownloadName = "image.png";
const MIN_SCALE = 1;
const MAX_SCALE = 6;

function applyViewerTransform() {
  viewerImage.style.transform = `translate(${viewerOffsetX}px, ${viewerOffsetY}px) scale(${viewerScale})`;
  document.getElementById("viewer-zoom-reset").textContent = `${Math.round(viewerScale * 100)}%`;
}

function resetViewerTransform() {
  viewerScale = 1;
  viewerOffsetX = 0;
  viewerOffsetY = 0;
  applyViewerTransform();
}

function setViewerScale(newScale) {
  viewerScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, newScale));
  if (viewerScale === MIN_SCALE) {
    viewerOffsetX = 0;
    viewerOffsetY = 0;
  }
  applyViewerTransform();
}

function openViewer(imgElement, title, downloadName) {
  if (!imgElement.src) return;
  viewerImage.src = imgElement.src;
  viewerImage.alt = imgElement.alt;
  viewerTitle.textContent = title;
  currentDownloadName = downloadName;
  resetViewerTransform();
  viewerOverlay.classList.remove("hidden");
  viewerOverlay.setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
  document.getElementById("viewer-close").focus();
}

function closeViewer() {
  viewerOverlay.classList.add("hidden");
  viewerOverlay.setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
  isPanning = false;
  if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
}

function openTargetById(targetId) {
  const img = document.getElementById(targetId);
  const figure = img.closest("figure");
  const title = figure.querySelector("figcaption").textContent;
  const downloadButton = figure.querySelector(`[data-download-target="${targetId}"]`);
  const filename = downloadButton?.getAttribute("data-download-name") || "image.png";
  openViewer(img, title, filename);
}

document.querySelectorAll("[data-viewer-target]").forEach((button) => {
  button.addEventListener("click", () => openTargetById(button.getAttribute("data-viewer-target")));
});

document.querySelectorAll("[data-open-image]").forEach((button) => {
  button.addEventListener("click", () => openTargetById(button.getAttribute("data-open-image")));
});

document.getElementById("viewer-close").addEventListener("click", closeViewer);
document.getElementById("viewer-zoom-in").addEventListener("click", () => setViewerScale(viewerScale + 0.5));
document.getElementById("viewer-zoom-out").addEventListener("click", () => setViewerScale(viewerScale - 0.5));
document.getElementById("viewer-zoom-reset").addEventListener("click", resetViewerTransform);

document.getElementById("viewer-fullscreen").addEventListener("click", () => {
  if (!document.fullscreenElement) viewerOverlay.requestFullscreen?.().catch(() => {});
  else document.exitFullscreen().catch(() => {});
});

document.addEventListener("keydown", (event) => {
  if (!viewerOverlay.classList.contains("hidden") && event.key === "Escape") closeViewer();
  if (!viewerOverlay.classList.contains("hidden") && event.key === "+") setViewerScale(viewerScale + 0.5);
  if (!viewerOverlay.classList.contains("hidden") && event.key === "-") setViewerScale(viewerScale - 0.5);
});

viewerOverlay.addEventListener("click", (event) => {
  if (event.target === viewerOverlay) closeViewer();
});

viewerStage.addEventListener("wheel", (event) => {
  event.preventDefault();
  setViewerScale(viewerScale + (event.deltaY > 0 ? -0.25 : 0.25));
}, { passive: false });

viewerStage.addEventListener("mousedown", (event) => {
  if (viewerScale <= MIN_SCALE) return;
  isPanning = true;
  panStartX = event.clientX - viewerOffsetX;
  panStartY = event.clientY - viewerOffsetY;
  viewerStage.classList.add("grabbing");
});

window.addEventListener("mousemove", (event) => {
  if (!isPanning) return;
  viewerOffsetX = event.clientX - panStartX;
  viewerOffsetY = event.clientY - panStartY;
  applyViewerTransform();
});

window.addEventListener("mouseup", () => {
  isPanning = false;
  viewerStage.classList.remove("grabbing");
});

function downloadDataUrl(dataUrl, filename) {
  if (!dataUrl) return;
  const link = document.createElement("a");
  link.href = dataUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
}

document.querySelectorAll("[data-download-target]").forEach((button) => {
  button.addEventListener("click", () => {
    const targetId = button.getAttribute("data-download-target");
    const img = document.getElementById(targetId);
    downloadDataUrl(img.src, button.getAttribute("data-download-name") || "image.png");
  });
});

document.getElementById("viewer-download").addEventListener("click", () => {
  downloadDataUrl(viewerImage.src, currentDownloadName);
});
