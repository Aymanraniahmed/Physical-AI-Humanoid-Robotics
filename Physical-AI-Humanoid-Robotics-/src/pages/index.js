import React, { useEffect, useRef } from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

// Animated particle background component
function ParticleBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const particleCount = 50;

    class Particle {
      constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 1;
        this.speedX = Math.random() * 0.5 - 0.25;
        this.speedY = Math.random() * 0.5 - 0.25;
        this.opacity = Math.random() * 0.5 + 0.2;
      }

      update() {
        this.x += this.speedX;
        this.y += this.speedY;

        if (this.x > canvas.width) this.x = 0;
        if (this.x < 0) this.x = canvas.width;
        if (this.y > canvas.height) this.y = 0;
        if (this.y < 0) this.y = canvas.height;
      }

      draw() {
        ctx.fillStyle = `rgba(0, 123, 255, ${this.opacity})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle());
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      particles.forEach(particle => {
        particle.update();
        particle.draw();
      });

      // Draw connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 100) {
            ctx.strokeStyle = `rgba(0, 212, 255, ${0.1 * (1 - distance / 100)})`;
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }

      requestAnimationFrame(animate);
    }

    animate();

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return <canvas ref={canvasRef} className={styles.particleCanvas} />;
}

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();

  return (
    <header className={styles.heroBanner}>
      <ParticleBackground />
      <div className={styles.heroOverlay}></div>

      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroLeft}>
            <div className={styles.badge} data-aos="fade-up">
              <span className={styles.badgeIcon}>🚀</span>
              <span>Advanced Physical AI Education</span>
            </div>

            <h1 className={styles.heroTitle} data-aos="fade-up" data-aos-delay="100">
              Physical AI &
              <br />
              <span className={styles.gradient}>Humanoid Robotics</span>
            </h1>

            <p className={styles.heroSubtitle} data-aos="fade-up" data-aos-delay="200">
              Transform Digital Intelligence into <strong>Embodied Action</strong>
            </p>

            <p className={styles.heroDescription} data-aos="fade-up" data-aos-delay="300">
              Master the complete robotics stack from ROS 2 fundamentals through cutting-edge
              Vision-Language-Action systems. Build autonomous humanoid robots that perceive,
              reason, and act in the physical world.
            </p>

            <div className={styles.techBadges} data-aos="fade-up" data-aos-delay="350">
              <span className={styles.techBadge}>ROS 2 Humble</span>
              <span className={styles.techBadge}>NVIDIA Isaac</span>
              <span className={styles.techBadge}>GPT-4 VLA</span>
              <span className={styles.techBadge}>Gazebo</span>
            </div>

            <div className={styles.buttons} data-aos="fade-up" data-aos-delay="400">
              <Link
                className={`button button--primary button--lg ${styles.primaryButton}`}
                to="/docs/intro/what-is-physical-ai">
                <span>Start Learning</span>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Link>

              <Link
                className={`button button--outline button--secondary button--lg ${styles.secondaryButton}`}
                to="https://github.com/yourusername/Physical-AI-Humanoid-Robotics">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
                <span>View on GitHub</span>
              </Link>
            </div>

            <div className={styles.stats} data-aos="fade-up" data-aos-delay="500">
              <div className={styles.stat}>
                <div className={styles.statNumber}>4</div>
                <div className={styles.statLabel}>Modules</div>
              </div>
              <div className={styles.stat}>
                <div className={styles.statNumber}>12</div>
                <div className={styles.statLabel}>Chapters</div>
              </div>
              <div className={styles.stat}>
                <div className={styles.statNumber}>50+</div>
                <div className={styles.statLabel}>Code Examples</div>
              </div>
            </div>
          </div>

          <div className={styles.heroRight} data-aos="fade-left" data-aos-delay="300">
            <div className={styles.heroImageContainer}>
              <div className={styles.glowingOrb}></div>
              <svg viewBox="0 0 500 600" className={styles.heroRobot}>
                <defs>
                  <linearGradient id="robotGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style={{stopColor: '#001F3F', stopOpacity: 1}} />
                    <stop offset="50%" style={{stopColor: '#007BFF', stopOpacity: 1}} />
                    <stop offset="100%" style={{stopColor: '#00D4FF', stopOpacity: 1}} />
                  </linearGradient>

                  <filter id="glow">
                    <feGaussianBlur stdDeviation="8" result="coloredBlur"/>
                    <feMerge>
                      <feMergeNode in="coloredBlur"/>
                      <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                  </filter>

                  <filter id="shadow">
                    <feDropShadow dx="0" dy="4" stdDeviation="8" floodColor="#007BFF" floodOpacity="0.5"/>
                  </filter>
                </defs>

                {/* Robot Body - Humanoid Form */}
                <g filter="url(#shadow)">
                  {/* Head */}
                  <rect x="200" y="50" width="100" height="80" rx="20" fill="url(#robotGradient)" opacity="0.95">
                    <animate attributeName="y" values="50;45;50" dur="3s" repeatCount="indefinite" />
                  </rect>

                  {/* Eyes with glow */}
                  <circle cx="230" cy="80" r="8" fill="#00D4FF" filter="url(#glow)">
                    <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="270" cy="80" r="8" fill="#00D4FF" filter="url(#glow)">
                    <animate attributeName="opacity" values="1;0.5;1" dur="2s" repeatCount="indefinite" />
                  </circle>

                  {/* Mouth/Interface */}
                  <rect x="220" y="100" width="60" height="4" rx="2" fill="#00D4FF" opacity="0.8"/>

                  {/* Neck */}
                  <rect x="230" y="130" width="40" height="30" rx="8" fill="url(#robotGradient)" opacity="0.9"/>

                  {/* Torso */}
                  <rect x="180" y="160" width="140" height="180" rx="25" fill="url(#robotGradient)" opacity="0.95"/>

                  {/* Core/Heart with pulse */}
                  <circle cx="250" cy="250" r="25" fill="none" stroke="#00D4FF" strokeWidth="3" opacity="0.8">
                    <animate attributeName="r" values="25;30;25" dur="2s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.8;0.3;0.8" dur="2s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="250" cy="250" r="15" fill="#00D4FF" opacity="0.6">
                    <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" />
                  </circle>

                  {/* Left Arm */}
                  <rect x="120" y="180" width="50" height="120" rx="15" fill="url(#robotGradient)" opacity="0.9">
                    <animateTransform attributeName="transform" type="rotate" values="0 145 180;-10 145 180;0 145 180" dur="4s" repeatCount="indefinite" />
                  </rect>
                  <rect x="125" y="300" width="40" height="80" rx="12" fill="url(#robotGradient)" opacity="0.85"/>

                  {/* Right Arm */}
                  <rect x="330" y="180" width="50" height="120" rx="15" fill="url(#robotGradient)" opacity="0.9">
                    <animateTransform attributeName="transform" type="rotate" values="0 355 180;10 355 180;0 355 180" dur="4s" repeatCount="indefinite" />
                  </rect>
                  <rect x="335" y="300" width="40" height="80" rx="12" fill="url(#robotGradient)" opacity="0.85"/>

                  {/* Pelvis */}
                  <rect x="190" y="340" width="120" height="60" rx="18" fill="url(#robotGradient)" opacity="0.9"/>

                  {/* Left Leg */}
                  <rect x="200" y="400" width="45" height="130" rx="15" fill="url(#robotGradient)" opacity="0.9"/>
                  <rect x="200" y="530" width="50" height="30" rx="12" fill="url(#robotGradient)" opacity="0.95"/>

                  {/* Right Leg */}
                  <rect x="255" y="400" width="45" height="130" rx="15" fill="url(#robotGradient)" opacity="0.9"/>
                  <rect x="250" y="530" width="50" height="30" rx="12" fill="url(#robotGradient)" opacity="0.95"/>
                </g>

                {/* Neural Network Connections */}
                <g opacity="0.4" stroke="#00D4FF" strokeWidth="2" fill="none">
                  <circle cx="80" cy="100" r="15">
                    <animate attributeName="r" values="15;18;15" dur="3s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="420" cy="300" r="20">
                    <animate attributeName="r" values="20;24;20" dur="3s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="100" cy="450" r="12">
                    <animate attributeName="r" values="12;15;12" dur="3s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="400" cy="150" r="18">
                    <animate attributeName="r" values="18;22;18" dur="3s" repeatCount="indefinite" />
                  </circle>

                  <path d="M 80 100 Q 140 120 180 160" strokeDasharray="5,5">
                    <animate attributeName="stroke-dashoffset" values="0;-10;0" dur="2s" repeatCount="indefinite" />
                  </path>
                  <path d="M 420 300 Q 360 280 320 260" strokeDasharray="5,5">
                    <animate attributeName="stroke-dashoffset" values="0;-10;0" dur="2s" repeatCount="indefinite" />
                  </path>
                </g>

                {/* Data Particles */}
                <g fill="#00D4FF">
                  <circle cx="50" cy="200" r="3" opacity="0.8">
                    <animate attributeName="cy" values="200;150;200" dur="4s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.8;0.2;0.8" dur="4s" repeatCount="indefinite" />
                  </circle>
                  <circle cx="450" cy="400" r="3" opacity="0.8">
                    <animate attributeName="cy" values="400;350;400" dur="3s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.8;0.2;0.8" dur="3s" repeatCount="indefinite" />
                  </circle>
                </g>
              </svg>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.scrollIndicator}>
        <div className={styles.mouse}>
          <div className={styles.mouseWheel}></div>
        </div>
        <span>Scroll to explore</span>
      </div>
    </header>
  );
}

function ModuleCard({ number, title, description, topics, color, delay }) {
  return (
    <div className={`${styles.moduleCard} ${styles[color]}`} data-aos="fade-up" data-aos-delay={delay}>
      <div className={styles.moduleHeader}>
        <div className={styles.moduleNumber}>Module {number}</div>
        <div className={styles.moduleIcon}>
          {number === '1' && '🤖'}
          {number === '2' && '🌐'}
          {number === '3' && '🧠'}
          {number === '4' && '🎯'}
        </div>
      </div>
      <h3 className={styles.moduleTitle}>{title}</h3>
      <p className={styles.moduleDescription}>{description}</p>
      <div className={styles.moduleTopics}>
        {topics.map((topic, idx) => (
          <span key={idx} className={styles.topic}>{topic}</span>
        ))}
      </div>
      <Link to={`/docs/module-${number}`} className={styles.moduleLink}>
        Explore Module <span>→</span>
      </Link>
    </div>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();

  useEffect(() => {
    // Initialize AOS (Animate On Scroll)
    if (typeof window !== 'undefined') {
      import('aos').then((AOS) => {
        AOS.init({
          duration: 800,
          once: true,
          offset: 100,
        });
      });
    }
  }, []);

  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Master Physical AI and Humanoid Robotics with ROS 2, NVIDIA Isaac, and VLA systems">
      <HomepageHeader />

      <main className={styles.mainContent}>
        {/* Learning Path */}
        <section className={styles.modulesSection}>
          <div className="container">
            <div className={styles.sectionHeader} data-aos="fade-up">
              <h2 className={styles.sectionTitle}>Your Learning Journey</h2>
              <p className={styles.sectionSubtitle}>
                Progress through 4 comprehensive modules, from fundamentals to cutting-edge VLA systems
              </p>
            </div>

            <div className={styles.modulesGrid}>
              <ModuleCard
                number="1"
                title="ROS 2 Fundamentals"
                description="The Robotic Nervous System"
                topics={['Nodes & Topics', 'Python rclpy', 'URDF Modeling']}
                color="blue"
                delay="0"
              />

              <ModuleCard
                number="2"
                title="Digital Twins"
                description="Simulation & Testing"
                topics={['Gazebo Physics', 'Unity Visualization', 'Sim-to-Real']}
                color="purple"
                delay="100"
              />

              <ModuleCard
                number="3"
                title="NVIDIA Isaac"
                description="GPU-Accelerated AI"
                topics={['Isaac Sim', 'Visual SLAM', 'Nav2 Planning']}
                color="green"
                delay="200"
              />

              <ModuleCard
                number="4"
                title="Vision-Language-Action"
                description="Autonomous Intelligence"
                topics={['Whisper Voice', 'GPT-4 Planning', 'Full Integration']}
                color="orange"
                delay="300"
              />
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className={styles.featuresSection}>
          <div className="container">
            <div className={styles.featuresGrid}>
              <div className={styles.featureItem} data-aos="fade-up" data-aos-delay="0">
                <div className={styles.featureIcon}>📖</div>
                <h3>12 Comprehensive Chapters</h3>
                <p>Progressive learning path from basics to advanced autonomous systems</p>
              </div>

              <div className={styles.featureItem} data-aos="fade-up" data-aos-delay="100">
                <div className={styles.featureIcon}>💻</div>
                <h3>50+ Code Examples</h3>
                <p>Production-ready Python code you can copy, modify, and deploy</p>
              </div>

              <div className={styles.featureItem} data-aos="fade-up" data-aos-delay="200">
                <div className={styles.featureIcon}>🚀</div>
                <h3>Complete Capstone Project</h3>
                <p>Build a voice-commanded autonomous humanoid from scratch</p>
              </div>

              <div className={styles.featureItem} data-aos="fade-up" data-aos-delay="300">
                <div className={styles.featureIcon}>🎓</div>
                <h3>Beginner-Friendly</h3>
                <p>No robotics experience required—just basic Python and AI knowledge</p>
              </div>
            </div>
          </div>
        </section>

        {/* Tech Stack Visualization */}
        <section className={styles.stackSection}>
          <div className="container">
            <h2 className={styles.sectionTitle} data-aos="fade-up">The Complete Stack</h2>
            <div className={styles.stackDiagram} data-aos="fade-up" data-aos-delay="100">
              <div className={styles.stackLayer} style={{animationDelay: '0s'}}>
                <div className={styles.layerLabel}>Application Layer</div>
                <div className={styles.layerContent}>Voice Commands + LLM Planning</div>
              </div>
              <div className={styles.stackLayer} style={{animationDelay: '0.1s'}}>
                <div className={styles.layerLabel}>Perception Layer</div>
                <div className={styles.layerContent}>Isaac ROS + Computer Vision</div>
              </div>
              <div className={styles.stackLayer} style={{animationDelay: '0.2s'}}>
                <div className={styles.layerLabel}>Simulation Layer</div>
                <div className={styles.layerContent}>Gazebo + Unity + Isaac Sim</div>
              </div>
              <div className={styles.stackLayer} style={{animationDelay: '0.3s'}}>
                <div className={styles.layerLabel}>Middleware Layer</div>
                <div className={styles.layerContent}>ROS 2 Humble (DDS)</div>
              </div>
              <div className={styles.stackLayer} style={{animationDelay: '0.4s'}}>
                <div className={styles.layerLabel}>Hardware Layer</div>
                <div className={styles.layerContent}>Sensors + Actuators + Compute</div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className={styles.ctaSection}>
          <div className="container">
            <div className={styles.ctaBox} data-aos="zoom-in">
              <h2 className={styles.ctaTitle}>Build the Future of Physical AI</h2>
              <p className={styles.ctaDescription}>
                Join the next generation of robotics engineers building autonomous humanoid systems
              </p>
              <Link
                className={`button button--primary button--lg ${styles.ctaButton}`}
                to="/docs/intro/what-is-physical-ai">
                <span>Start Your Journey</span>
                <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </Link>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
