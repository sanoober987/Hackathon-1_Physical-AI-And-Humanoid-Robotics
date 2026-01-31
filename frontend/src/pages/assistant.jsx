import React, { Suspense, useState, useEffect } from 'react';
import Layout from '@theme/Layout';

// Dynamically import ChatWidget for client-side only
const ChatWidget = React.lazy(() => import('../components/ChatWidget'));

// Error Boundary Component
class ChatErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ChatWidget Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '2rem',
          textAlign: 'center',
          backgroundColor: '#fee2e2',
          color: '#dc2626',
          borderRadius: '12px',
          border: '1px solid #fecaca',
          margin: '1rem'
        }}>
          <h3 style={{ marginBottom: '0.5rem' }}>⚠️ Chat Widget Error</h3>
          <p style={{ margin: 0, fontSize: '0.9rem' }}>
            The chat widget is currently unavailable. Please refresh the page or try again later.
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

function AssistantPage() {
  const [locale] = useState('en'); // Always use English since we removed Urdu

  // Get messages based on locale
  const t = {
    title: "AI-Powered Physical AI Assistant",
    description: "Advanced AI assistant for Physical AI & Humanoid Robotics textbook with RAG capabilities",
    heading: "AI-Powered Physical AI Assistant",
    subtitle: "Advanced AI assistant powered by RAG technology. Ask questions about Physical AI, robotics, and humanoid systems. Our intelligent assistant understands context and provides precise answers from the textbook.",
    powered_by: "Powered by Retrieval-Augmented Generation (RAG) technology • Real-time context retrieval • Context-aware responses",
    features: ["RAG Technology", "Context-Aware", "Real-Time Answers", "Personalized"]
  };

  return (
    <Layout
      title={t.title}
      description={t.description}>
      <div className="assistant-container" style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '2rem 0',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Animated background elements */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at top right, rgba(255,255,255,0.1) 0%, transparent 50%), radial-gradient(circle at bottom left, rgba(255,255,255,0.1) 0%, transparent 50%)',
          zIndex: 1
        }} />

        <div style={{ position: 'relative', zIndex: 2 }}>
          {/* Hero Section */}
          <div style={{
            maxWidth: '1200px',
            width: '100%',
            margin: '0 auto',
            padding: '0 20px',
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}>
            <div style={{
              textAlign: 'center',
              marginBottom: '3rem',
              marginTop: '2rem',
              position: 'relative'
            }}>
              <div style={{
                position: 'absolute',
                top: '-3rem',
                left: '50%',
                transform: 'translateX(-50%)',
                width: '80px',
                height: '80px',
                background: 'linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%)',
                borderRadius: '50%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 10px 30px rgba(0, 0, 0, 0.2)',
                animation: 'float 6s ease-in-out infinite',
                backdropFilter: 'blur(10px)',
                WebkitBackdropFilter: 'blur(10px)'
              }}>
                <span style={{ fontSize: '2rem', color: '#667eea' }}>🤖</span>
              </div>

              <h1 style={{
                fontSize: '3rem',
                fontWeight: '800',
                color: 'white',
                marginBottom: '1rem',
                textShadow: '0 2px 4px rgba(0,0,0,0.3)',
                animation: 'fadeInUp 0.8s ease-out'
              }}>
                {t.heading}
              </h1>

              <p style={{
                fontSize: '1.4rem',
                color: 'rgba(255, 255, 255, 0.9)',
                maxWidth: '700px',
                margin: '0 auto 2rem',
                lineHeight: '1.7',
                animation: 'fadeInUp 0.8s ease-out 0.2s both'
              }}>
                {t.subtitle}
              </p>

              {/* Features Grid */}
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1.5rem',
                maxWidth: '800px',
                margin: '2rem auto',
                animation: 'fadeInUp 0.8s ease-out 0.3s both'
              }}>
                {t.features.map((feature, index) => (
                  <div
                    key={index}
                    style={{
                      background: 'rgba(255, 255, 255, 0.15)',
                      backdropFilter: 'blur(10px)',
                      WebkitBackdropFilter: 'blur(10px)',
                      padding: '1rem',
                      borderRadius: '16px',
                      border: '1px solid rgba(255, 255, 255, 0.2)',
                      transition: 'all 0.3s ease',
                      cursor: 'default'
                    }}
                    className="glass-card"
                  >
                    <div style={{
                      fontSize: '1.2rem',
                      marginBottom: '0.5rem',
                      color: 'rgba(255, 255, 255, 0.9)'
                    }}>
                      ✨
                    </div>
                    <div style={{
                      fontWeight: '600',
                      color: 'white'
                    }}>
                      {feature}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Chat Widget */}
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              width: '100%',
              maxWidth: '900px',
              animation: 'fadeInUp 0.8s ease-out 0.4s both',
              position: 'relative'
            }}>
              <div style={{
                width: '100%',
                maxWidth: '500px',
                height: '700px',
                border: 'none',
                borderRadius: '24px',
                overflow: 'hidden',
                position: 'relative',
                background: 'rgba(255, 255, 255, 0.1)',
                backdropFilter: 'blur(20px)',
                WebkitBackdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.2)'
              }}>
                <div style={{
                  position: 'absolute',
                  top: '0',
                  left: '0',
                  right: '0',
                  bottom: '0',
                  background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
                  borderRadius: '24px',
                  zIndex: 1
                }} />
                <div style={{
                  position: 'relative',
                  zIndex: 3,
                  height: '100%'
                }}>
                  <Suspense fallback={
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      height: '100%',
                      background: 'rgba(255, 255, 255, 0.1)',
                      backdropFilter: 'blur(10px)',
                      WebkitBackdropFilter: 'blur(10px)',
                      borderRadius: '24px',
                      border: '1px solid rgba(255, 255, 255, 0.2)'
                    }}>
                      <div style={{
                        textAlign: 'center',
                        color: 'white'
                      }}>
                        <div style={{
                          fontSize: '2rem',
                          marginBottom: '1rem',
                          animation: 'pulse 2s infinite'
                        }}>⏳</div>
                        <div style={{ fontSize: '1.1rem' }}>
                          Loading AI Assistant...
                        </div>
                        <div style={{
                          fontSize: '0.9rem',
                          opacity: 0.8,
                          marginTop: '0.5rem'
                        }}>
                          Preparing your personalized experience
                        </div>
                      </div>
                    </div>
                  }>
                    <ChatErrorBoundary locale={locale}>
                      <ChatWidget standalone={true} locale={locale} />
                    </ChatErrorBoundary>
                  </Suspense>
                </div>
              </div>
            </div>

            {/* Footer Info */}
            <div style={{
              marginTop: '3rem',
              textAlign: 'center',
              color: 'rgba(255, 255, 255, 0.8)',
              fontSize: '0.9rem',
              maxWidth: '700px',
              animation: 'fadeInUp 0.8s ease-out 0.6s both',
              opacity: 0.8
            }}>
              <p>{t.powered_by}</p>
            </div>
          </div>
        </div>

        <style jsx>{`
          @keyframes fadeInUp {
            from {
              opacity: 0;
              transform: translateY(30px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          @keyframes float {
            0% { transform: translateX(-50%) translateY(0px); }
            50% { transform: translateX(-50%) translateY(-10px); }
            100% { transform: translateX(-50%) translateY(0px); }
          }

          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
          }

          .assistant-container {
            position: relative;
            overflow: hidden;
          }

          .assistant-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image:
              radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 40% 80%, rgba(255, 255, 255, 0.03) 0%, transparent 50%);
            pointer-events: none;
          }
        `}</style>
      </div>
    </Layout>
  );
}

export default AssistantPage;