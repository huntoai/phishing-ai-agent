import * as React from "react"
import Layout from "../components/layout"
import Seo from "../components/seo"
import Hero from "../components/compound/Hero"
import { Card } from "../components/elements"

const features = [
  {
    icon: "🎓",
    title: "Gamified Learning",
    description: "Learn about phishing through interactive, Duolingo-style lessons with streaks, points, and achievements."
  },
  {
    icon: "📱",
    title: "Multi-Platform Delivery",
    description: "Get awareness drip content on WhatsApp, email, and more. No login required - all progress saved locally."
  },
  {
    icon: "🚨",
    title: "Report Scams",
    description: "Easily report suspicious messages and get real-time guidance on next steps including government and bank reporting."
  },
  {
    icon: "📚",
    title: "Scam Encyclopedia",
    description: "Browse a comprehensive, TLDRLegal-style database of different scam types with clear explanations."
  },
  {
    icon: "🤖",
    title: "AI-Powered Detection",
    description: "Leverage advanced AI to identify and analyze phishing attempts with 98% accuracy."
  },
  {
    icon: "🔒",
    title: "Privacy First",
    description: "Your data stays local until you choose to sync. No tracking, no personal data collection."
  }
]

const IndexPage = () => (
  <Layout>
    <Hero />
    
    <section style={{ 
      padding: '4rem 2rem',
      maxWidth: '1280px',
      margin: '0 auto'
    }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h2 style={{ 
          fontSize: '2.5rem',
          fontWeight: '700',
          marginBottom: '1rem',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text'
        }}>
          Everything You Need to Stay Safe
        </h2>
        <p style={{ 
          fontSize: '1.125rem',
          color: '#cbd5e1',
          maxWidth: '700px',
          margin: '0 auto'
        }}>
          Comprehensive tools and resources to protect yourself and others from phishing attacks
        </p>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        marginBottom: '4rem'
      }}>
        {features.map((feature, index) => (
          <Card key={index} variant="glass" hover={true}>
            <div style={{ 
              fontSize: '3rem',
              marginBottom: '1rem'
            }}>
              {feature.icon}
            </div>
            <h3 style={{
              fontSize: '1.25rem',
              fontWeight: '600',
              marginBottom: '0.75rem',
              color: '#f8fafc'
            }}>
              {feature.title}
            </h3>
            <p style={{
              color: '#cbd5e1',
              lineHeight: '1.6'
            }}>
              {feature.description}
            </p>
          </Card>
        ))}
      </div>
    </section>
  </Layout>
)

export const Head = () => <Seo title="Home - Phishing Awareness Platform" />

export default IndexPage
