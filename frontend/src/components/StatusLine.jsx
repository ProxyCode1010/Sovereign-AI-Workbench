import React from 'react';

export default function StatusLine({ text, loading }) {
  if (!text && !loading) return <div className="execution-row" />;

  return (
    <div className={`execution-row ${loading ? 'is-running' : ''}`}>
      {loading && <div className="execution-spinner" />}
      <span>{text}</span>
    </div>
  );
}
