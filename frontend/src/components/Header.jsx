import React from 'react';

export default function Header({ backendStatus }) {
  return (
    <>
      <header className="top-header">
        <div className="brand-block">
          <div className="brand-mark">SW</div>
          <div className="brand-info">
            <h1 className="brand-title">Sovereign AI Workbench</h1>
            <span className="brand-subtext">Air-Gapped Engineering Operations</span>
          </div>
        </div>

        <div className="header-status-area">
          {backendStatus === 'online' ? (
            <div className="badge-clean status-online">
              <span className="status-square" />
              <span>System Online</span>
            </div>
          ) : backendStatus === 'offline' ? (
            <div className="badge-clean status-offline">
              <span className="status-square" />
              <span>Backend Offline</span>
            </div>
          ) : (
            <div className="badge-clean" style={{ color: 'var(--c-peach)' }}>
              <span className="status-square" />
              <span>Checking...</span>
            </div>
          )}

          <a
            href="https://smith.langchain.com"
            target="_blank"
            rel="noopener noreferrer"
            className="badge-clean telemetry-link"
            title="Open LangSmith Tracing Console"
          >
            <span>LangSmith Tracing Active</span>
            <span style={{ fontSize: '12px' }}>↗</span>
          </a>
        </div>
      </header>

      <section className="overview-bar">
        <div className="overview-container">
          <div className="overview-description">
            On-premise zero-outbound intelligence environment executing local multi-model routing, isolated Docker execution, and cryptographic vector citations.
          </div>

          <div className="overview-metrics">
            <div className="metric-box">
              <span className="metric-box-label">Network Guard</span>
              <span className="metric-box-value">Enforced Air-Gap</span>
            </div>
            <div className="metric-box">
              <span className="metric-box-label">Active Models</span>
              <span className="metric-box-value">Qwen 2.5 / Moondream</span>
            </div>
            <div className="metric-box">
              <span className="metric-box-label">Execution Sandbox</span>
              <span className="metric-box-value">Docker Non-Networked</span>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
