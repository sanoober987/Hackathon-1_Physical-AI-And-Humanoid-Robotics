import React from 'react';

const Module4 = ({ isUrduEnabled }) => {
  const urduContent = `
    وژن لینگویج ایکشن (VLA) ماڈلز ایسے AI ماڈلز ہیں جو تصاویر (وژن)، زبان (لینگویج)،
    اور حرکت (ایکشن) کو ایک انٹیگریٹڈ ڈھانچے میں جوڑتے ہیں۔ یہ ماڈلز فزیکل دنیا میں
    براہ راست تعامل کے لیے ضروری ہیں کیونکہ وہ تبصرے کو سمجھ سکتے ہیں، ماحول کا تجزیہ کر سکتے ہیں،
    اور مطابق حرکتیں انجام دے سکتے ہیں۔

    VLA ماڈلز کے اجزاء:
    - وژن انکوڈر: تصاویر کو سمجھنے کے لیے
    - لینگویج انکوڈر: تبصرے کو سمجھنے کے لیے
    - ایکشن ڈیکوڈر: مناسب حرکتیں تیار کرنے کے لیے

    VLA کے اطلاقات:
    - ہوم اسسٹنٹ روبوٹس
    - صنعتی خودکار کارروائیاں
    - تعلیمی روبوٹس
    - دیکھ بھال کے روبوٹس
  `;

  const englishContent = `
    <h2 class="section-title">Vision-Language-Action Models</h2>
    <div class="section-content">
      <p>Vision-Language-Action (VLA) models are AI models that integrate vision (images), language (text), and action (motor control) in a unified framework. These models are essential for direct interaction in the physical world as they can understand commands, analyze environments, and execute appropriate actions.</p>

      <h3>Components of VLA Models:</h3>
      <ul>
        <li>Vision encoder: To understand images</li>
        <li>Language encoder: To understand commands</li>
        <li>Action decoder: To generate appropriate motor actions</li>
      </ul>

      <h3>Applications of VLA:</h3>
      <ul>
        <li>Home assistant robots</li>
        <li>Industrial automation</li>
        <li>Educational robots</li>
        <li>Caregiving robots</li>
      </ul>

      <h3>Technical Challenges:</h3>
      <p>VLA models face challenges in multimodal alignment, temporal consistency, and real-time inference. They require large-scale datasets of paired vision-language-action triplets and sophisticated architectures to effectively map between modalities while maintaining causality and safety in physical interactions.</p>
    </div>
  `;

  return (
    <div className="module-wrapper">
      <div className="module-header">
        <h1 className="module-title">Module 4: Vision-Language-Action Models</h1>
        <p className="module-description">Multimodal AI models for physical interaction</p>
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

export default Module4;