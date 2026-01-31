import React from 'react';

const Module1 = () => {
  const content = `
    <h2 class="section-title">ROS 2 Fundamentals</h2>
    <div class="section-content">
      <p>ROS 2 (Robot Operating System 2) is an open-source meta operating system for robotics software development. It provides hardware abstraction, modular software components, and an integrated distributed framework. ROS 2 features a DDS (Data Distribution Service) based communication architecture that allows reliable, real-time data exchange.</p>

      <h3>Core Components of ROS 2:</h3>
      <ul>
        <li><strong>Nodes:</strong> Computational units of a robot system</li>
        <li><strong>Topics:</strong> Used for data sharing between nodes</li>
        <li><strong>Services:</strong> Request-reply mechanism for synchronous communication</li>
        <li><strong>Actions:</strong> Long-running tasks with feedback and goal management</li>
      </ul>

      <h3>New Features in ROS 2:</h3>
      <ul>
        <li>Security support for safe deployments</li>
        <li>Reliability for industrial applications</li>
        <li>Performance improvements for low latency</li>
        <li>Quality of service policies for flexible communication</li>
      </ul>

      <h3>ROS 2 Architecture:</h3>
      <p>The ROS 2 architecture consists of client libraries (rclcpp, rclpy), a middleware layer (RMW), and the DDS implementation. This layered approach provides flexibility and portability across different DDS implementations while maintaining a consistent API.</p>
    </div>
  `;

  return (
    <div className="module-wrapper">
      <div className="module-header">
        <h1 className="module-title">Module 1: ROS 2 Fundamentals</h1>
        <p className="module-description">Introduction to Robot Operating System 2 and its ecosystem</p>
      </div>

      <div className="module-body">
        <div className="english-content" dangerouslySetInnerHTML={{ __html: content }} />
      </div>
    </div>
  );
};

export default Module1;