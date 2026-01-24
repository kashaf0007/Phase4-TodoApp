// frontend/src/components/ToolCallDisplay.jsx
import React from 'react';

const ToolCallDisplay = ({ toolCalls }) => {
  if (!toolCalls || toolCalls.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        marginTop: '10px',
        padding: '10px',
        backgroundColor: '#f8f9fa',
        borderRadius: '6px',
        borderLeft: '4px solid #007bff',
        fontSize: '0.85em',
        overflowX: 'auto'
      }}
      role="region"
      aria-label="Tool execution details"
    >
      <strong style={{ color: '#007bff', display: 'block', marginBottom: '5px' }}>Tools Used:</strong>
      <ul style={{
        margin: '5px 0 0 0',
        padding: '0 0 0 20px',
        listStyleType: 'disc'
      }}>
        {toolCalls.map((toolCall, index) => (
          <li key={index} style={{ margin: '5px 0', wordBreak: 'break-word' }}>
            <span style={{ fontWeight: 'bold', display: 'inline-block', minWidth: '80px' }}>
              {toolCall.tool_name}:
            </span>
            <span
              style={{
                fontFamily: 'monospace',
                backgroundColor: '#e9ecef',
                padding: '2px 6px',
                borderRadius: '4px',
                fontSize: '0.8em'
              }}
              aria-label={`Parameters: ${JSON.stringify(toolCall.parameters)}`}
            >
              {JSON.stringify(toolCall.parameters)}
            </span>
            {toolCall.result && (
              <div style={{ marginTop: '4px', color: '#28a745' }}>
                <span style={{ fontWeight: 'bold', display: 'inline-block', minWidth: '80px' }}>
                  Result:
                </span>
                <span style={{ wordBreak: 'break-word' }}>
                  {JSON.stringify(toolCall.result)}
                </span>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ToolCallDisplay;