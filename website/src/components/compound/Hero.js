import React from 'react';
import { Link } from 'gatsby';
import { Button } from '../elements';
import * as styles from './Hero.module.css';

const Hero = () => {
  return (
    <section className={styles.hero}>
      <div className={styles.container}>
        <div className={styles.content}>
          <h1 className={styles.title}>
            Protect Yourself From
            <span className={styles.gradientText}> Phishing Attacks</span>
          </h1>
          <p className={styles.subtitle}>
            Learn, identify, and report phishing scams with our AI-powered
            awareness platform. Get gamified training, real-time scam
            reporting, and comprehensive scam education.
          </p>
          <div className={styles.buttonGroup}>
            <Link to="/learn">
              <Button size="large">Start Learning Free</Button>
            </Link>
            <Link to="/report">
              <Button variant="secondary" size="large">
                Report a Scam
              </Button>
            </Link>
          </div>
          <div className={styles.stats}>
            <div className={styles.stat}>
              <div className={styles.statValue}>10K+</div>
              <div className={styles.statLabel}>Users Protected</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statValue}>5K+</div>
              <div className={styles.statLabel}>Scams Reported</div>
            </div>
            <div className={styles.stat}>
              <div className={styles.statValue}>98%</div>
              <div className={styles.statLabel}>Detection Rate</div>
            </div>
          </div>
        </div>
        <div className={styles.illustration}>
          <div className={styles.glowOrb}></div>
          <div className={styles.floatingCard}>
            <div className={styles.cardIcon}>🔒</div>
            <div className={styles.cardText}>Secure</div>
          </div>
          <div className={styles.floatingCard2}>
            <div className={styles.cardIcon}>🎯</div>
            <div className={styles.cardText}>Accurate</div>
          </div>
          <div className={styles.floatingCard3}>
            <div className={styles.cardIcon}>⚡</div>
            <div className={styles.cardText}>Fast</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
