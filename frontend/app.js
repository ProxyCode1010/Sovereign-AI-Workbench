const API = "http://localhost:8000/api";
let uploadedFilename = null;

// ---------- helpers ----------
function setStatus(id, text, loading) {
  const el = document.getElementById(id);
  el.classList.toggle("loading", !!loading);
  el.querySelector(".statusText").textContent = text;
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str == null ? "" : String(str);
  return div.innerHTML;
}

// ---------- routing panel helpers ----------
async function animateRouting(panelId) {
  const panel = document.getElementById(panelId);
  panel.classList.add("show");
  panel.innerHTML = `<div class="routing-step"><span class="icon">🔍</span> Analyzing query intent…</div>`;
  await new Promise(r => setTimeout(r, 400));
}

function renderRouting(panelId, { category, method, model }) {
  const panel = document.getElementById(panelId);
  panel.classList.add("show");

  const methodLabel =
    method === "llm_agent"
      ? '<span class="method-tag agent">🧠 agent reasoned</span>'
      : method === "keyword"
      ? '<span class="method-tag">⚡ keyword match</span>'
      : method === "image_flag"
      ? '<span class="method-tag">🖼️ image detected</span>'
      : "";

  panel.innerHTML = `
    <div class="routing-step"><span class="icon">🔍</span> Analyzed query intent ${methodLabel}</div>
    <div class="routing-step"><span class="icon">🏷️</span> Classified as: <b>${escapeHtml(category)}</b></div>
    <div class="routing-final">→ Routed to model: ${escapeHtml(model)}</div>
  `;
}

// ---------- health check ----------
async function checkHealth() {
  const badge = document.getElementById("healthBadge");
  try {
    const res = await fetch(`${API}/health`);
    if (res.ok) {
      badge.className = "badge";
      badge.innerHTML = '<span class="dot"></span> backend online — air-gapped';
    } else {
      throw new Error("bad status");
    }
  } catch {
    badge.className = "badge offline";
    badge.innerHTML = '<span class="dot"></span> backend unreachable — run docker compose up -d';
  }
}
checkHealth();

// ---------- Section 1: scan -> approval note ----------
async function uploadScan() {
  const fileInput = document.getElementById("scanFile");
  const file = fileInput.files[0];
  if (!file) {
    setStatus("inspectionStatus", "Choose a file first.", false);
    return;
  }

  setStatus("inspectionStatus", "Uploading…", true);
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API}/upload`, { method: "POST", body: formData });
    const data = await res.json();
    uploadedFilename = file.name;

    document.getElementById("uploadedName").textContent = file.name;
    document.getElementById("uploadedTag").classList.add("show");
    document.getElementById("genNoteBtn").disabled = false;

    setStatus("inspectionStatus", "Uploaded. Ready to generate.", false);
  } catch (e) {
    setStatus("inspectionStatus", "Upload failed: " + e.message, false);
  }
}

async function runInspection() {
  if (!uploadedFilename) return;

  await animateRouting("inspectionRouting");
  setStatus("inspectionStatus", "Running OCR + vision model + drafting note (can take 20–40s)…", true);
  document.getElementById("inspectionResult").classList.remove("show");

  const formData = new FormData();
  formData.append("scan_filename", uploadedFilename);
  formData.append("title", "Inspection Approval Note");

  try {
    const res = await fetch(`${API}/agent/inspection-to-note`, { method: "POST", body: formData });
    const data = await res.json();
    setStatus("inspectionStatus", "Done.", false);

    renderRouting("inspectionRouting", {
      category: data.routing_category,
      method: data.routing_method,
      model: data.model_used,
    });

    const findingsHtml = (data.findings || [])
      .map(f => "• " + escapeHtml(f))
      .join("\n");

    const box = document.getElementById("inspectionResult");
    box.innerHTML = `
      <div class="label">Key findings</div>
      <div class="value">${findingsHtml || "(none extracted)"}</div>
      <div class="label">Recommendation</div>
      <div class="value">${escapeHtml(data.recommendation)}</div>
      <div class="label">Output file</div>
      <div class="value mono">${escapeHtml(data.output_file)}</div>
    `;
    box.classList.add("show");
  } catch (e) {
    setStatus("inspectionStatus", "Failed: " + e.message, false);
  }
}

// ---------- Section 2: coding agent ----------
async function runCode() {
  const description = document.getElementById("codeTask").value.trim();
  if (!description) {
    setStatus("codeStatus", "Enter a task description first.", false);
    return;
  }

  await animateRouting("codeRouting");
  setStatus("codeStatus", "Generating code and running in sandbox (can take 20–60s)…", true);
  document.getElementById("codeResult").classList.remove("show");

  const formData = new FormData();
  formData.append("description", description);

  try {
    const res = await fetch(`${API}/agent/code-task`, { method: "POST", body: formData });
    const data = await res.json();
    setStatus("codeStatus", "Done.", false);

    renderRouting("codeRouting", {
      category: data.routing_category,
      method: data.routing_method,
      model: data.model_used,
    });

    const exitCode = data.sandbox_result ? data.sandbox_result.exit_code : undefined;
    const exitOk = exitCode === 0;

    const box = document.getElementById("codeResult");
    box.innerHTML = `
      <div class="label">Generated code</div>
      <div class="value mono">${escapeHtml(data.code)}</div>
      <div class="label">Sandbox result</div>
      <div class="value">Exit code: <span class="${exitOk ? "exit-ok" : "exit-fail"}">${escapeHtml(exitCode)}</span></div>
      <div class="value mono">${escapeHtml(data.sandbox_result ? data.sandbox_result.output : "")}</div>
    `;
    box.classList.add("show");
  } catch (e) {
    setStatus("codeStatus", "Failed: " + e.message, false);
  }
}

// ---------- Section 3: RAG ----------
async function runRag() {
  const question = document.getElementById("ragQuestion").value.trim();
  if (!question) {
    setStatus("ragStatus", "Type a question first.", false);
    return;
  }

  await animateRouting("ragRouting");
  setStatus("ragStatus", "Searching knowledge base and generating answer…", true);
  document.getElementById("ragResult").classList.remove("show");

  const formData = new FormData();
  formData.append("question", question);

  try {
    const res = await fetch(`${API}/agent/rag-query`, { method: "POST", body: formData });
    const data = await res.json();
    setStatus("ragStatus", "Done.", false);

    renderRouting("ragRouting", {
      category: data.routing_category,
      method: data.routing_method,
      model: data.model_used,
    });

    const sourcesHtml = (data.sources || [])
      .map(s => `<span class="source-chip">${escapeHtml(s.split("/").pop())}</span>`)
      .join("");

    const box = document.getElementById("ragResult");
    box.innerHTML = `
      <div class="label">Answer</div>
      <div class="value">${escapeHtml(data.answer)}</div>
      <div class="label">Sources</div>
      <div class="sources">${sourcesHtml || "<span style='color:var(--text-dim)'>none retrieved</span>"}</div>
    `;
    box.classList.add("show");
  } catch (e) {
    setStatus("ragStatus", "Failed: " + e.message, false);
  }
}