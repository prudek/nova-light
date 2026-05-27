const platformSelect = document.getElementById("platform-select");
const releaseLabel = document.getElementById("release-label");
const installButton = document.getElementById("install-button");
const manualLink = document.getElementById("manual-download-link");
const releaseNotes = document.getElementById("release-notes");
const olderReleases = document.getElementById("older-releases");

function renderMarkdown(text) {
  if (window.marked && typeof window.marked.parse === "function") {
    return window.marked.parse(text);
  }
  return `<pre>${text}</pre>`;
}

function renderOlderReleases(releases) {
  if (!releases || releases.length <= 1) {
    olderReleases.innerHTML = "";
    return;
  }

  const rows = releases
    .slice(1)
    .map(
      (release) =>
        `<li><a href="${release.html_url}" target="_blank" rel="noreferrer">${release.tag}</a> · ${new Date(release.published_at).toLocaleDateString()}</li>`,
    )
    .join("");

  olderReleases.innerHTML = `<strong>Older releases</strong><ul>${rows}</ul>`;
}

function applyPlatform(release, platformId) {
  const platform = release.platforms[platformId];
  if (!platform) {
    return;
  }

  if (platform.web_manifest_url) {
    installButton.setAttribute("manifest", platform.web_manifest_url);
  } else {
    installButton.removeAttribute("manifest");
  }

  if (platform.merged_bin_url) {
    manualLink.href = platform.merged_bin_url;
    manualLink.style.pointerEvents = "auto";
    manualLink.style.opacity = "1";
  } else {
    manualLink.removeAttribute("href");
    manualLink.style.pointerEvents = "none";
    manualLink.style.opacity = "0.5";
  }
}

function bootstrap(index) {
  const latest = index.latest;
  if (!latest) {
    releaseLabel.textContent = "no release published yet";
    releaseNotes.innerHTML = "<p>No release metadata available.</p>";
    return;
  }

  releaseLabel.textContent = `${latest.tag} (${new Date(latest.published_at).toLocaleDateString()})`;
  releaseNotes.innerHTML = renderMarkdown(latest.body || `# ${latest.tag}\n\nNo notes provided.`);
  renderOlderReleases(index.releases);

  const platformEntries = Object.values(latest.platforms || {});
  platformSelect.innerHTML = platformEntries
    .map((platform) => `<option value="${platform.platform_id}">${platform.label}</option>`)
    .join("");

  const defaultPlatform = platformEntries.find((p) => p.platform_id === "esp32-esp-wroom-32") || platformEntries[0];
  if (!defaultPlatform) {
    return;
  }

  platformSelect.value = defaultPlatform.platform_id;
  applyPlatform(latest, defaultPlatform.platform_id);
  platformSelect.addEventListener("change", () => applyPlatform(latest, platformSelect.value));
}

fetch("./releases.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  })
  .then(bootstrap)
  .catch((error) => {
    releaseLabel.textContent = "failed to load release index";
    releaseNotes.innerHTML = `<p>Could not load release metadata: ${String(error)}</p>`;
  });
