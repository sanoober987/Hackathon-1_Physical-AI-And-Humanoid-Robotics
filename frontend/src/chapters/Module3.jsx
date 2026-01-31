import React from 'react';

const Module3 = ({ isUrduEnabled }) => {
  const urduContent = `
    NVIDIA Isaac ایک مکمل روبوٹکس ڈویلپمنٹ پلیٹ فارم ہے جو روبوٹکس ایپلی کیشنز کو تیار کرنے،
    سیمولاٹ کرنے، اور اسے حقیقی دنیا میں چلانے کے لیے ٹولز، لائبریریز، اور SDKs فراہم کرتا ہے۔
    یہ پلیٹ فارم NVIDIA CUDA، TensorRT، اور GPU ایکسلریشن کے ذریعے AI ماڈلز کو بہتر بناتا ہے۔

    Isaac پلیٹ فارم کے اجزاء:
    - Isaac Sim: ہائی فیڈلٹی سیمولیشن ٹول
    - Isaac ROS: ROS 2 کے لیے GPU ایکسلریٹڈ لائبریریز
    - Isaac Lab: روبوٹکس ڈویلپمنٹ کے لیے ٹولز

    NVIDIA Isaac کے فوائد:
    - GPU ایکسلریشن کے ذریعے AI کارکردگی
    - حقیقی دنیا کی طرح سیمولیشن
    - آسان AI ماڈلز کو ڈیپلوئی کرنا
    - ایک انٹیگریٹڈ ڈویلپمنٹ ورک فلو
  `;

  const englishContent = `
    <h2 class="section-title">NVIDIA Isaac Platform</h2>
    <div class="section-content">
      <p>NVIDIA Isaac is a comprehensive robotics development platform that provides tools, libraries, and SDKs for creating, simulating, and deploying robotics applications. The platform leverages NVIDIA CUDA, TensorRT, and GPU acceleration to enhance AI models for robotics.</p>

      <h3>Isaac Platform Components:</h3>
      <ul>
        <li>Isaac Sim: High-fidelity simulation tool</li>
        <li>Isaac ROS: GPU-accelerated libraries for ROS 2</li>
        <li>Isaac Lab: Tools for robotics development</li>
      </ul>

      <h3>Benefits of NVIDIA Isaac:</h3>
      <ul>
        <li>AI performance through GPU acceleration</li>
        <li>Photorealistic simulation environments</li>
        <li>Easy deployment of AI models</li>
        <li>Integrated development workflow</li>
      </ul>

      <h3>Isaac Sim Features:</h3>
      <p>Isaac Sim provides realistic physics simulation, photorealistic rendering, and seamless integration with popular robotics frameworks. It supports reinforcement learning, imitation learning, and synthetic data generation for training AI models in virtual environments before deployment.</p>
    </div>
  `;

  return (
    <div className="module-wrapper">
      <div className="module-header">
        <h1 className="module-title">Module 3: NVIDIA Isaac Platform</h1>
        <p className="module-description">GPU-accelerated robotics development platform</p>
      </div>

      <div className="module-body">
        {isUrduEnabled ? (
          <div className="urdu-content" dangerouslySetInnerHTML={{ __html: urduContent }} />
        ) : (
          <div className="english-content" dangerouslySetInnerHTML={{ __html: englishContent }} />
        )}
      </div>
    </div>
  );
};

export default Module3;