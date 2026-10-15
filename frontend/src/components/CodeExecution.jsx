import React, { useState } from 'react';
import RoutingPanel from './RoutingPanel';
import StatusLine from './StatusLine';

export default function CodeExecution({ apiBase }) {
  const [description, setDescription] = useState(
    'Write a function to calculate pipe wall thickness per ASME B31.3 given pressure, diameter, and allowable stress, then print a test result'
  );
  const [status, setStatus] = useState({ text: '', loading: false });
  const [routing, setRouting] = useState(null);
  const [isRouting, setIsRouting] = useState(false);
  const [result, setResult] = useState(null);

  const runCode = async () => {
    if (!description.trim()) {
      setStatus({ text: 'Please enter a task description.', loading: false });
      return;
    }

    setIsRouting(true);
    setStatus({
      text: 'Synthesizing Python code & running in non-networked Docker container (20–40s)…',
      loading: true,
    });
    setResult(null);

    const formData = new FormData();
    formData.append('description', description.trim());

    try {
      const res = await fetch(`${apiBase}/agent/code-task`, {
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
      setStatus({ text: 'Execution completed.', loading: false });
    } catch (e) {
      setIsRouting(false);
      setStatus({ text: `Execution failed: ${e.message}`, loading: false });
    }
  };

  const exitCode = result?.sandbox_result?.exit_code;
  const exitOk = exitCode === 0;

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-header-left">
          <span className="panel-index">02</span>
          <div>
            <h2 className="panel-title">Isolated Code Sandbox Engine</h2>
            <p className="panel-description">Synthesize engineering logic and execute inside an isolated container with zero network access.</p>
          </div>
        </div>
        <span className="panel-category-tag">Docker Sandbox</span>
      </div>

      <div className="panel-body">
        <label className="field-label">Engineering Specification or Computation Task</label>
        
        <textarea
          className="field-textarea"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe the calculation or algorithm..."
        />

        <div className="button-row">
          <button 
            className="btn btn-navy" 
            onClick={runCode} 
            disabled={status.loading}
          >
            Run in Sandbox
          </button>
        </div>

        <RoutingPanel routing={routing} isRouting={isRouting} />
        <StatusLine text={status.text} loading={status.loading} />

        {result && (
          <div className="result-block">
            <div className="result-section-label">Generated Code</div>
            <pre className="code-box">{result.code}</pre>

            <div className="result-section-label">Sandbox Output</div>
            <div style={{ marginBottom: '6px' }}>
              Exit Status:{' '}
              <span className={`exit-badge ${exitOk ? 'zero' : 'nonzero'}`}>
                {exitCode !== undefined ? `Exit Code ${exitCode}` : 'N/A'}
              </span>
            </div>

            <pre className="code-box stdout">
              {result.sandbox_result?.output || '(Process completed without output)'}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
