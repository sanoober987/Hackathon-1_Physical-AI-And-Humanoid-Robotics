import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import clsx from 'clsx';

const Home = () => {
  const { siteConfig } = useDocusaurusContext();

  const features = [
    {
      icon: "🧠",
      title: "Advanced AI",
      description: "Learn state-of-the-art AI techniques for physical systems and embodied cognition"
    },
    {
      icon: "🤖",
      title: "Humanoid Robotics",
      description: "Master the complexities of humanoid robot control, gait, and human-like interaction"
    },
    {
      icon: "🌐",
      title: "ROS 2 Framework",
      description: "Deep dive into the industry-standard robotics platform for real-world applications"
    },
    {
      icon: "⚡",
      title: "Real-time Systems",
      description: "Build responsive systems for real-time physical AI applications"
    },
    {
      icon: "🔬",
      title: "Sensor Integration",
      description: "Understand how sensors and actuators enable intelligent physical interaction"
    },
    {
      icon: "🎯",
      title: "Embodied Learning",
      description: "Explore how AI learns through physical interaction with the real world"
    }
  ];

  return (
    <Layout
      title="Physical AI & Humanoid Robotics Academy"
      description="A Comprehensive Textbook on Physical AI and Humanoid Robotics">
      <div className="hero hero--primary" style={{ position: 'relative', overflow: 'hidden' }}>
        {/* Animated background elements */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'radial-gradient(circle at top right, rgba(102, 126, 234, 0.1) 0%, rgba(255, 255, 255, 0) 50%), radial-gradient(circle at bottom left, rgba(118, 75, 162, 0.1) 0%, rgba(255, 255, 255, 0) 50%)',
          zIndex: 1
        }} />

        <div className="container" style={{ position: 'relative', zIndex: 2 }}>
          <div className="row" style={{ alignItems: 'center', minHeight: '80vh' }}>
            <div className="col col--6 padding--lg">
              <div className="margin-bottom--lg">
                <h1 className="hero__title" style={{
                  fontSize: '3.5rem',
                  fontWeight: '800',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  marginBottom: '1rem'
                }}>
                  Physical AI & Humanoid Robotics
                </h1>
                <p className="hero__subtitle" style={{
                  fontSize: '1.4rem',
                  lineHeight: '1.6',
                  color: 'rgba(255, 255, 255, 0.9)',
                  marginBottom: '2rem'
                }}>
                  Master the cutting-edge technologies that are shaping the future of human-robot interaction and intelligent systems
                </p>
                <div className="margin-top--lg" style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                  <Link
                    className="button button--primary button--lg"
                    to="/docs/intro"
                    style={{
                      borderRadius: '50px',
                      padding: '1rem 2rem',
                      fontSize: '1.1rem',
                      fontWeight: '600'
                    }}>
                    Start Learning
                  </Link>
                  <Link
                    className="button button--secondary button--lg"
                    to="/assistant"
                    style={{
                      borderRadius: '50px',
                      padding: '1rem 2rem',
                      fontSize: '1.1rem',
                      fontWeight: '600',
                      background: 'rgba(255, 255, 255, 0.15)',
                      backdropFilter: 'blur(10px)',
                      border: '1px solid rgba(255, 255, 255, 0.2)'
                    }}>
                    AI Assistant
                  </Link>
                </div>
              </div>
            </div>
            <div className="col col--6 padding--lg">
              <div style={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%'
              }}>
                <div style={{
                  width: '100%',
                  maxWidth: '400px',
                  height: '400px',
                  background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: '24px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  position: 'relative',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    fontSize: '8rem',
                    opacity: 0.1,
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)'
                  }}>
                    🤖
                  </div>
                  <div style={{
                    textAlign: 'center',
                    zIndex: 1
                  }}>
                    <div style={{ fontSize: '4rem', marginBottom: '1rem', filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.2))' }}>🤖</div>
                    <h3 style={{ color: 'white', fontSize: '1.5rem', fontWeight: '600' }}>Humanoid Robot</h3>
                    <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '1rem' }}>Next-Gen AI Integration</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <section className="padding-top--xl padding-bottom--xl" style={{ background: 'var(--ifm-color-emphasis-100)' }}>
        <div className="container">
          <div className="row">
            <div className="col col--12 text--center margin-bottom--xl">
              <h2 className="text--center" style={{
                fontSize: '2.5rem',
                fontWeight: '700',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                marginBottom: '1rem'
              }}>
                Why Learn Physical AI & Robotics?
              </h2>
              <p className="text--center" style={{ fontSize: '1.2rem', color: 'var(--ifm-color-emphasis-700)' }}>
                Master the cutting-edge technologies that are shaping the future of human-robot interaction and intelligent systems
              </p>
            </div>
          </div>

          <div className="row">
            {features.map((feature, index) => (
              <div key={index} className="col col--4 margin-bottom--lg">
                <div className="card glass-card" style={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  textAlign: 'center',
                  padding: '2rem',
                  background: 'rgba(255, 255, 255, 0.1)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255, 255, 255, 0.15)',
                  borderRadius: '16px'
                }}>
                  <div style={{ fontSize: '3rem', marginBottom: '1.5rem' }}>{feature.icon}</div>
                  <h3 style={{
                    fontSize: '1.4rem',
                    fontWeight: '600',
                    marginBottom: '1rem',
                    color: 'var(--ifm-color-primary)'
                  }}>{feature.title}</h3>
                  <p style={{ color: 'var(--ifm-color-emphasis-700)', lineHeight: '1.6' }}>
                    {feature.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Textbook Section */}
      <section className="padding-top--xl padding-bottom--xl">
        <div className="container">
          <div className="row">
            <div className="col col--12 text--center margin-bottom--xl">
              <h2 style={{
                fontSize: '2.5rem',
                fontWeight: '700',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                marginBottom: '1rem'
              }}>
                Complete Textbook Access
              </h2>
              <p style={{ fontSize: '1.2rem', color: 'var(--ifm-color-emphasis-700)', maxWidth: '600px', margin: '0 auto 2rem' }}>
                Access the full Physical AI & Humanoid Robotics textbook with comprehensive chapters covering all essential topics.
              </p>
              <Link
                className="button button--primary button--lg"
                to="/docs/intro"
                style={{
                  borderRadius: '50px',
                  padding: '1rem 2rem',
                  fontSize: '1.1rem',
                  fontWeight: '600',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                }}>
                Read Textbook
              </Link>
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
};

export default Home;