import React from 'react';

const Module2 = () => {
  const content = `
    <h2 class="section-title">Digital Twin Technology</h2>
    <div class="section-content">
      <p>A digital twin is a virtual representation that connects the physical and digital worlds by linking real-time data with its digital counterpart. This technology is crucial in robotics as it enhances robot design, manufacturing, testing, and operation.</p>

      <h3>Benefits of Digital Twins:</h3>
      <ul>
        <li>Rapid prototyping and testing of models</li>
        <li>Virtual testing to reduce risks</li>
        <li>Performance optimization through data analysis</li>
        <li>Real-time monitoring and predictive maintenance</li>
      </ul>

      <h3>Components of Digital Twins:</h3>
      <ul>
        <li>Physical entity: The real-world version</li>
        <li>Virtual twin: The digital model</li>
        <li>Connection: Data flow between both entities</li>
      </ul>

      <h3>Applications in Robotics:</h3>
      <p>Digital twins in robotics enable virtual testing of robot behaviors, prediction of maintenance needs, and optimization of operational parameters. They allow for comprehensive simulation before physical deployment, reducing costs and risks associated with real-world testing.</p>
    </div>
  `;

  return (
    <div className="module-wrapper">
      <div className="module-header">
        <h1 className="module-title">Module 2: Digital Twin Technology</h1>
        <p className="module-description">Virtual representations connecting physical and digital worlds</p>
      </div>

      <div className="module-body">
        <div className="english-content" dangerouslySetInnerHTML={{ __html: content }} />
      </div>
    </div>
  );
};

export default Module2;