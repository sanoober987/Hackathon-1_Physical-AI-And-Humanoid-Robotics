import React, { Suspense } from 'react';
import Layout from '@theme/Layout';

// Dynamically import ChatWidget for client-side only
const ChatWidget = React.lazy(() => import('../components/ChatWidget'));

function ChatPage() {
  // Define animation styles
  const fadeInUpAnimation = {
    animation: 'fadeInUp 0.8s ease-out'
  };

  const slideInUpAnimation = {
    animation: 'slideInUp 1s ease-out'
  };

  // Inject CSS animations into the document
  React.useEffect(() => {
    const style = document.createElement('style');
    style.innerHTML = `
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

      @keyframes slideInUp {
        from {
          opacity: 0;
          transform: translateY(50px) scale(0.95);
        }
        to {
          opacity: 1;
          transform: translateY(0) scale(1);
        }
      }
    `;
    document.head.appendChild(style);

    return () => {
      document.head.removeChild(style);
    };
  }, []);

  return (
    <Layout
      title={`Physical AI Chatbot`}
      description="Interactive chatbot for Physical AI & Humanoid Robotics textbook">
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: 'linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%)',
        padding: '2rem 0'
      }}>
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
            ...fadeInUpAnimation,
            textAlign: 'center',
            marginBottom: '3rem',
            marginTop: '2rem',
          }}>
            <h1 style={{
              fontSize: '2.8rem',
              fontWeight: '700',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
              marginBottom: '1rem',
              textShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              Physical AI & Humanoid Robotics Assistant
            </h1>
            <p style={{
              fontSize: '1.3rem',
              color: '#606770',
              maxWidth: '700px',
              margin: '0 auto',
              lineHeight: '1.6',
              textShadow: '0 1px 2px rgba(0,0,0,0.05)'
            }}>
              Ask questions about Physical AI, robotics, and humanoid systems. Our AI assistant will help you understand complex concepts from the textbook in English or Urdu.
            </p>
          </div>

          <div style={{
            ...slideInUpAnimation,
            display: 'flex',
            justifyContent: 'center',
            width: '100%',
            maxWidth: '900px',
          }}>
            <div style={{
              width: '100%',
              maxWidth: '500px',
              height: '700px',
              border: 'none',
              borderRadius: '16px',
              boxShadow: '0 20px 40px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.2)',
              overflow: 'hidden',
              background: 'rgba(255, 255, 255, 0.95)',
              backdropFilter: 'blur(10px)'
            }}>
              <Suspense fallback={<div>Loading chat widget...</div>}>
                <ChatWidget standalone={true} />
              </Suspense>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default ChatPage;