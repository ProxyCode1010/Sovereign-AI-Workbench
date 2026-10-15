import React, { useState, useRef } from 'react';
import RoutingPanel from './RoutingPanel';
import StatusLine from './StatusLine';

export default function DocumentAnalysis({ apiBase }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadedFilename, setUploadedFilename] = useState(null);
  const [status, setStatus] = useState({ text: '', loading: false });
  const [routing, setRouting] = useState(null);
  const [isRouting, setIsRouting] = useState(false);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const uploadScan = async () => {
    if (!selectedFile) {
      setStatus({ text: 'Please select a technical document or inspection image first.', loading: false });
      return;
    }

    setStatus({ text: 'Uploading file to local staging storage…', loading: true });
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await fetch(`${apiBase}/upload`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await res.json();
      setUploadedFilename(selectedFile.name);
      setStatus({ text: `File "${selectedFile.name}" staged successfully.`, loading: false });
    } catch (e) {
      setStatus({ text: `Upload failed: ${e.message}`, loading: false });
    }
  };

  const runInspection = async () => {
    if (!uploadedFilename) return;

    setIsRouting(true);
    setStatus({
      text: 'Running OCR & multi-model vision synthesis (can take 20–40s)…',
      loading: true,
    });
    setResult(null);

    const formData = new FormData();
    formData.append('scan_filename', uploadedFilename);
    formData.append('title', 'Inspection Approval Note');

    try {
      const res = await fetch(`${apiBase}/agent/inspection-to-note`, {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();

      setIsRouting(false);
      setRouting({
        category: data.routing_category,
        method: data.routing_method,
        model: data.model_used,
      });
      setResult(data);
      setStatus({ text: 'Processing complete. Document generated.', loading: false });
    } catch (e) {
      setIsRouting(false);
      setStatus({ text: `Processing failed: ${e.message}`, loading: false });
    }
  };

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-header-left">
          <span className="panel-index">01</span>
          <div>
            <h2 className="panel-title">Document Analysis & Approval Generator</h2>
            <p className="panel-description">Extract findings from scanned engineering reports and draft formal approval notes.</p>
          </div>
        </div>
        <span className="panel-category-tag">Vision & OCR Pipeline</span>
      </div>

      <div className="panel-body">
        <label className="field-label">Inspection Document or Technical Drawing</label>
        
        <div 
          className="upload-box" 
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="upload-box-title">
            {selectedFile ? selectedFile.name : 'Choose a file or drag & drop (PDF, PNG, JPG)'}
          </div>
          <div className="upload-box-help">
            Zero cloud transmission — processed exclusively within local container memory
          </div>
        </div>

        <input 
          ref={fileInputRef}
          type="file" 
          accept="image/*,.pdf" 
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />

        {uploadedFilename && (
          <div className="file-selected-indicator">
            <span>Staged in local storage:</span>
            <b>{uploadedFilename}</b>
          </div>
        )}

        <div className="button-row">
          <button 
            className="btn btn-outline" 
            onClick={uploadScan}
            disabled={status.loading || !selectedFile}
          >
            Upload to Staging
          </button>
          <button 
            className="btn btn-berry" 
            onClick={runInspection} 
            disabled={!uploadedFilename || status.loading}
          >
            Generate Approval Note (.docx)
          </button>
        </div>

        <RoutingPanel routing={routing} isRouting={isRouting} />
        <StatusLine text={status.text} loading={status.loading} />

        {result && (
          <div className="result-block">
            <div className="result-section-label">Key Findings</div>
            <div className="result-section-text">
              {result.findings && result.findings.length > 0 ? (
                result.findings.map((finding, idx) => (
                  <div key={idx} style={{ marginBottom: '4px' }}>• {finding}</div>
                ))
              ) : (
                <div>(No findings parsed)</div>
              )}
            </div>

            <div className="result-section-label">Technical Recommendation</div>
            <div className="result-section-text" style={{ fontWeight: 600, color: 'var(--c-navy)' }}>
              {result.recommendation}
            </div>

            <div className="result-section-label">Generated File</div>
            <pre className="code-box stdout">{result.output_file}</pre>
          </div>
        )}
      </div>
    </div>
  );
}
