import React from 'react';

function ExampleDialog({ examples }) {
  return (
    <div className="example-dialog">
      <h2>Real-Life Examples</h2>
      <ul>
        {examples.map((example, index) => (
          <li key={index}>{example}</li>
        ))}
      </ul>
    </div>
  );
}

export default ExampleDialog;
