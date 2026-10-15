import React from 'react';

export default function RoutingPanel({ routing, isRouting }) {
  if (isRouting) {
    return (
      <div className="routing-strip">
        <div className="routing-strip-header">Router Decision</div>
        <div>Evaluating task intent to dispatch to the correct sovereign model…</div>
      </div>
    );
  }

  if (!routing) return null;

  const { category, method, model } = routing;

  const methodText =
    method === 'llm_agent'
      ? 'LLM Reasoning'
      : method === 'keyword'
      ? 'Rule-Based Keyword'
      : method === 'image_flag'
      ? 'Image Detection'
      : method;

  return (
    <div className="routing-strip">
      <div className="routing-strip-header">Router Telemetry</div>
      <div className="routing-strip-details">
        <div className="routing-meta-tag">
          <span>Method:</span>
          <b>{methodText}</b>
        </div>
        <div className="routing-meta-tag">
          <span>Category:</span>
          <b>{category}</b>
        </div>
        <div className="routing-meta-tag">
          <span>Target Model:</span>
          <span className="routing-chip">{model}</span>
        </div>
      </div>
    </div>
  );
}
