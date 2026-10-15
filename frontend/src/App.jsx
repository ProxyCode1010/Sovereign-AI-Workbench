import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import DocumentAnalysis from './components/DocumentAnalysis';
import CodeExecution from './components/CodeExecution';
import KnowledgeBaseRAG from './components/KnowledgeBaseRAG';

const API_BASE = 'http://localhost:8000/api';

export default function App() {
  const [backendStatus, setBackendStatus] = useState('checking');
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
          setBackendStatus('online');
        } else {
          setBackendStatus('offline');
        }
      } catch {
        setBackendStatus('offline');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 8000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-shell">
      <Header backendStatus={backendStatus} />

      <main className="workbench-content">
        {/* Professional Navigation Tabs */}
        <nav className="tabs-header">
          <button 
            className={`tab-item ${activeTab === 'all' ? 'active' : ''}`}
            onClick={() => setActiveTab('all')}
          >
            All Workflows <span className="tab-count">3</span>
          </button>
          <button 
            className={`tab-item ${activeTab === 'vision' ? 'active' : ''}`}
            onClick={() => setActiveTab('vision')}
          >
            01 Document & OCR
          </button>
          <button 
            className={`tab-item ${activeTab === 'code' ? 'active' : ''}`}
            onClick={() => setActiveTab('code')}
          >
            02 Code Sandbox
          </button>
          <button 
            className={`tab-item ${activeTab === 'rag' ? 'active' : ''}`}
            onClick={() => setActiveTab('rag')}
          >
            03 Knowledge Base
          </button>
        </nav>

        {/* Workflow Panels */}
        {(activeTab === 'all' || activeTab === 'vision') && (
          <DocumentAnalysis apiBase={API_BASE} />
        )}

        {(activeTab === 'all' || activeTab === 'code') && (
          <CodeExecution apiBase={API_BASE} />
        )}

        {(activeTab === 'all' || activeTab === 'rag') && (
          <KnowledgeBaseRAG apiBase={API_BASE} />
        )}
      </main>

      <footer className="app-footer">
        <div className="footer-container">
          <div>
            <b>Sovereign AI Workbench</b> &mdash; Air-gapped on-premise operations console.
          </div>
          <div>
            Observability via <a className="footer-link" href="https://smith.langchain.com" target="_blank" rel="noreferrer">LangSmith Tracing</a> | Docker Guard Active
          </div>
        </div>
      </footer>
    </div>
  );
}
