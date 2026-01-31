const express = require('express');
const cors = require('cors');
const path = require('path');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
  origin: '*',
  credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Mock RAG service for Physical AI knowledge
class MockRAGService {
  constructor() {
    this.knowledgeBase = [
      {
        id: 1,
        title: "Introduction to Physical AI",
        content: "Physical AI combines artificial intelligence with physical systems, focusing on embodied cognition, sensorimotor learning, and real-world interaction. Unlike traditional AI, Physical AI must deal with the complexities of physics, uncertainty, and real-time constraints.",
        category: "Physical AI Concepts"
      },
      {
        id: 2,
        title: "Humanoid Robotics",
        content: "Humanoid robots are designed to resemble humans in appearance and behavior. They typically have a head, torso, two arms, and two legs. The challenge lies in achieving stable bipedal locomotion, natural movement, and human-like interaction capabilities.",
        category: "Robotics"
      },
      {
        id: 3,
        title: "Sensors and Actuators",
        content: "Robots rely on sensors to perceive their environment and actuators to interact with it. Common sensors include cameras, LiDAR, IMUs, force/torque sensors, and tactile sensors. Actuators include motors, servos, and pneumatic/hydraulic systems.",
        category: "Hardware Components"
      },
      {
        id: 4,
        title: "ROS2 Framework",
        content: "ROS2 (Robot Operating System 2) is a flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robot platforms.",
        category: "Software Frameworks"
      },
      {
        id: 5,
        title: "Gait Control",
        content: "Gait control in humanoid robots involves managing the walking pattern and maintaining balance. It requires sophisticated algorithms to handle the dynamic stability of bipedal locomotion, including swing phase control, stance phase management, and transition between steps.",
        category: "Locomotion"
      }
    ];
  }

  async search(query, topK = 3) {
    // Simple keyword matching for demo purposes
    const queryLower = query.toLowerCase();
    return this.knowledgeBase
      .filter(item =>
        item.title.toLowerCase().includes(queryLower) ||
        item.content.toLowerCase().includes(queryLower)
      )
      .slice(0, topK);
  }

  async generateAnswer(question, context, language = 'en') {
    // Simulate AI response generation based on context
    const responseTemplates = {
      en: [
        `Based on the Physical AI textbook, ${context}. This concept is fundamental to understanding how artificial intelligence can be embodied in physical systems.`,
        `According to the knowledge base, ${context}. This is particularly relevant in the field of humanoid robotics and embodied AI.`,
        `The Physical AI textbook explains that ${context}. This principle is essential for developing intelligent physical systems.`
      ],
      ur: [
        `فزیکل ای آئی کے مطابق، ${context}۔ یہ اس بات کو سمجھنے کے لیے بنیادی ہے کہ مصنوعی ذہانت کو جسمانی نظام میں کیسے جامہ پوش کیا جا سکتا ہے۔`,
        `ذخیرہ علم کے مطابق، ${context}۔ یہ ہیومنوائڈ روبوٹکس اور جسمانی ای آئی کے شعبے میں خاص طور پر متعلق ہے۔`,
        `فزیکل ای آئی کے نصاب میں وضاحت کی گئی ہے کہ ${context}۔ جسمانی نظام تیار کرنے کے لیے یہ اصول ضروری ہے۔`
      ]
    };

    const templates = responseTemplates[language] || responseTemplates.en;
    const randomTemplate = templates[Math.floor(Math.random() * templates.length)];

    // Replace context placeholder with actual content if it's generic
    if (context.includes('Based on the')) {
      return `I found relevant information about "${question}". The Physical AI Assistant can provide detailed insights about physical AI concepts, robotics, sensors, actuators, and humanoid systems.`;
    }

    return randomTemplate;
  }
}

const ragService = new MockRAGService();

// Routes
app.get('/', (req, res) => {
  res.json({
    message: 'AI-Powered Physical AI Assistant API',
    status: 'healthy',
    version: '1.0.0',
    endpoints: {
      'POST /assistant/chat': 'Chat with the Physical AI Assistant',
      'GET /assistant/health': 'Health check endpoint',
      'GET /assistant/capabilities': 'Get assistant capabilities'
    }
  });
});

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'AI-Powered Physical AI Assistant',
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

app.get('/assistant/capabilities', (req, res) => {
  res.json({
    capabilities: [
      'Natural language understanding for Physical AI concepts',
      'Multi-language support (English and Urdu)',
      'Context-aware responses using RAG',
      'Knowledge of robotics, sensors, actuators, and humanoid systems',
      'Real-time information retrieval',
      'Intelligent question answering'
    ],
    supportedLanguages: ['en', 'ur'],
    knowledgeDomains: [
      'Physical AI concepts',
      'Robotics fundamentals',
      'Sensors and actuators',
      'Humanoid systems',
      'ROS2 framework',
      'Gait control and locomotion'
    ]
  });
});

app.post('/assistant/chat', async (req, res) => {
  try {
    const { question, user_id, language = 'en', context = null } = req.body;

    if (!question) {
      return res.status(400).json({
        error: 'Question is required',
        message: 'Please provide a question to answer'
      });
    }

    // Search for relevant context in knowledge base
    const searchResults = await ragService.search(question);

    // Generate response based on context
    let response;
    let sources = [];

    if (searchResults.length > 0) {
      const bestMatch = searchResults[0];
      response = await ragService.generateAnswer(question, bestMatch.content, language);
      sources = searchResults.map(result => ({
        id: result.id,
        title: result.title,
        category: result.category,
        relevance: Math.random() // Mock relevance score
      }));
    } else {
      // Fallback response when no context found
      const fallbackResponses = {
        en: `I'm sorry, but I couldn't find specific information about "${question}" in my knowledge base. The Physical AI Assistant specializes in topics related to physical AI, robotics, sensors, actuators, and humanoid systems. Feel free to ask about these topics!`,
        ur: `معذرت، لیکن میں اپنے علم کے ذخیرے میں "${question}" کے بارے میں مخصوص معلومات تلاش نہیں کر سکا۔ فزیکل ای آئی اسسٹنٹ جسمانی ای آئی، روبوٹکس، سینسرز، ایکچوایٹرز، اور ہیومنوائڈ سسٹمز سے متعلق موضوعات میں مہارت رکھتا ہے۔ ان موضوعات کے بارے میں پوچھنا چاہیں!`
      };

      response = fallbackResponses[language] || fallbackResponses.en;
    }

    res.json({
      response,
      sources,
      question,
      language,
      user_id: user_id || 'anonymous',
      timestamp: new Date().toISOString(),
      confidence: Math.min(0.95, 0.7 + Math.random() * 0.25) // Mock confidence score
    });

  } catch (error) {
    console.error('Error processing chat request:', error);
    const errorResponses = {
      en: 'I encountered an error while processing your request. Please try again or rephrase your question.',
      ur: 'آپ کی درخواست کو پروسیس کرتے وقت مجھے ایک خرابی کا سامنا کرنا پڑا۔ براہ کرم دوبارہ کوشش کریں یا اپنا سوال دوبارہ بیان کریں۔'
    };

    res.status(500).json({
      error: 'Internal server error',
      message: errorResponses[language || 'en'],
      timestamp: new Date().toISOString()
    });
  }
});

// Streaming chat endpoint
app.post('/api/v1/chat/stream', async (req, res) => {
  try {
    const { question, user_id, language = 'en', context = null } = req.body;

    if (!question) {
      return res.status(400).json({
        error: 'Question is required',
        message: 'Please provide a question to answer'
      });
    }

    // Set headers for streaming response
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Transfer-Encoding', 'chunked');

    // Search for relevant context in knowledge base
    const searchResults = await ragService.search(question);

    // Send sources first if any
    if (searchResults.length > 0) {
      const sources = searchResults.map(result => ({
        id: result.id,
        title: result.title,
        section: result.category,
        relevance: Math.random() // Mock relevance score
      }));

      res.write(`data: ${JSON.stringify({ type: 'sources', sources })}\n\n`);
    }

    // Simulate streaming response by breaking it into chunks
    const generateAnswerChunks = (question, content, lang) => {
      const templates = {
        en: [
          `Based on the Physical AI textbook, ${content}. This concept is fundamental to understanding how artificial intelligence can be embodied in physical systems.`,
          `According to the knowledge base, ${content}. This is particularly relevant in the field of humanoid robotics and embodied AI.`,
          `The Physical AI textbook explains that ${content}. This principle is essential for developing intelligent physical systems.`
        ],
        ur: [
          `فزیکل ای آئی کے مطابق، ${content}۔ یہ اس بات کو سمجھنے کے لیے بنیادی ہے کہ مصنوعی ذہانت کو جسمانی نظام میں کیسے جامہ پوش کیا جا سکتا ہے۔`,
          `ذخیرہ علم کے مطابق، ${content}۔ یہ ہیومنوائڈ روبوٹکس اور جسمانی ای آئی کے شعبے میں خاص طور پر متعلق ہے۔`,
          `فزیکل ای آئی کے نصاب میں وضاحت کی گئی ہے کہ ${content}۔ جسمانی نظام تیار کرنے کے لیے یہ اصول ضروری ہے۔`
        ]
      };

      const templatesForLang = templates[lang] || templates.en;
      const randomTemplate = templatesForLang[Math.floor(Math.random() * templatesForLang.length)];

      // If content is generic, provide a more specific response
      if (content.includes('Based on the')) {
        return `I found relevant information about "${question}". The Physical AI Assistant can provide detailed insights about physical AI concepts, robotics, sensors, actuators, and humanoid systems.`;
      }

      return randomTemplate;
    };

    let response;
    if (searchResults.length > 0) {
      const bestMatch = searchResults[0];
      response = generateAnswerChunks(question, bestMatch.content, language);
    } else {
      const fallbackResponses = {
        en: `I'm sorry, but I couldn't find specific information about "${question}" in my knowledge base. The Physical AI Assistant specializes in topics related to physical AI, robotics, sensors, actuators, and humanoid systems. Feel free to ask about these topics!`,
        ur: `معذرت، لیکن میں اپنے علم کے ذخیرے میں "${question}" کے بارے میں مخصوص معلومات تلاش نہیں کر سکا۔ فزیکل ای آئی اسسٹنٹ جسمانی ای آئی، روبوٹکس، سینسرز، ایکچوایٹرز، اور ہیومنوائڈ سسٹمز سے متعلق موضوعات میں مہارت رکھتا ہے۔ ان موضوعات کے بارے میں پوچھنا چاہیں!`
      };
      response = fallbackResponses[language] || fallbackResponses.en;
    }

    // Stream the response character by character to simulate real-time typing
    const sendToken = (token) => {
      res.write(`data: ${JSON.stringify({ type: 'token', token })}\n\n`);
    };

    // Send response in chunks to simulate streaming
    const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

    for (let i = 0; i < response.length; i++) {
      const char = response[i];
      sendToken(char);

      // Small delay to simulate typing
      await delay(10 + Math.random() * 20);
    }

    // Send done signal
    res.write(`data: ${JSON.stringify({ type: 'done' })}\n\n`);
    res.end();

  } catch (error) {
    console.error('Error processing streaming chat request:', error);

    // Send error as stream data
    res.write(`data: ${JSON.stringify({ type: 'error', message: 'An error occurred while processing your request.' })}\n\n`);
    res.end();
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: 'An unexpected error occurred. Please try again.'
  });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({
    error: 'Route not found',
    message: `The requested endpoint ${req.originalUrl} does not exist.`
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`AI-Powered Physical AI Assistant server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
  console.log(`API root: http://localhost:${PORT}/`);
});

module.exports = app;