import React, { useState } from 'react';
import RoutingPanel from './RoutingPanel';
import StatusLine from './StatusLine';

export default function KnowledgeBaseRAG({ apiBase }) {
  const [question, setQuestion] = useState('What is the procedure for emergency equipment shutdown?');
  const [status, setStatus] = useState({ text: '', loading: false });
  const [routing, setRouting] = useState(null);
  const [isRouting, setIsRouting] = useState(false);
  const [result, setResult] = useState(null);

  const ingestKB = async () => {
    setStatus({ text: 'Indexing documents into local pgvector database…', loading: true });
    try {
      const res = await fetch(`${apiBase}/kb/ingest`, { method: 'POST' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const count = data.ingested?.length || 0;
      setStatus({ 
        text: `Indexed ${count} documents into local vector storage.`, 
        loading: false 
      });
    } catch (e) {
      setStatus({ text: `Indexing failed: ${e.message}`, loading: false });
    }
  };

  const runRag = async () => {
    if (!question.trim()) {
      setStatus({ text: 'Please enter an inquiry question.', loading: false });
      return;
    }

    setIsRouting(true);
    setStatus({
      text: 'Retrieving context vectors & drafting grounded answer…',
      loading: true,
    });
    setResult(null);

    const formData = new FormData();
    formData.append('question', question.trim());

    try {
      const res = await fetch(`${apiBase}/agent/rag-query`, {
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
      setStatus({ text: 'Query resolved with verified local document citations.', loading: false });
    } catch (e) {
      setIsRouting(false);
      setStatus({ text: `Query failed: ${e.message}`, loading: false });
    }
  };

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-header-left">
          <span className="panel-index">03</span>
          <div>
            <h2 className="panel-title">Air-Gapped Knowledge Base (RAG)</h2>
            <p className="panel-description">Query internal standard operating procedures and technical manuals with strict citation grounding.</p>
          </div>
        </div>
        <span className="panel-category-tag">pgvector RAG</span>
      </div>

      <div className="panel-body">
        <label className="field-label">Natural Language Inquiry</label>
        
        <input
          type="text"
          className="field-input"
          placeholder="e.g. What is the SOP for valve isolation?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') runRag();
          }}
        />

        <div className="button-row">
          <button 
            className="btn btn-navy" 
            onClick={runRag} 
            disabled={status.loading}
          >
            Query Knowledge Base
          </button>
          <button 
            className="btn btn-outline" 
            onClick={ingestKB} 
            disabled={status.loading}
          >
            Re-Index Documents
          </button>
        </div>

        <RoutingPanel routing={routing} isRouting={isRouting} />
        <StatusLine text={status.text} loading={status.loading} />

        {result && (
          <div className="result-block">
            <div className="result-section-label">Grounded Answer</div>
            <div className="result-section-text" style={{ fontSize: '13.5px' }}>
              {result.answer}
            </div>

            <div className="result-section-label">Source Citations</div>
            <div className="sources-container">
              {result.sources && result.sources.length > 0 ? (
                result.sources.map((src, idx) => (
                  <span key={idx} className="citation-chip">
                    {src.split('/').pop()}
                  </span>
                ))
              ) : (
                <span style={{ color: 'var(--text-secondary)' }}>No source documents retrieved</span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
