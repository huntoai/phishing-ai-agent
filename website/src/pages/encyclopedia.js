import * as React from "react"
import { useState } from "react"
import Layout from "../components/layout"
import Seo from "../components/seo"
import { Card, Button, Input, Badge } from "../components/elements"
import { scamTypes, scamCategories } from "../data/scamsData"
import * as styles from "./encyclopedia.module.css"

const EncyclopediaPage = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedScam, setSelectedScam] = useState(null)

  const filteredScams = scamTypes.filter(scam => {
    const matchesSearch = searchQuery === '' || 
      scam.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      scam.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      scam.tldr.toLowerCase().includes(searchQuery.toLowerCase())
    
    const matchesCategory = selectedCategory === 'all' || 
      scam.category.toLowerCase().replace(' ', '-') === selectedCategory

    return matchesSearch && matchesCategory
  })

  if (selectedScam) {
    const scam = selectedScam
    return (
      <Layout>
        <div className={styles.encyclopediaPage}>
          <Button 
            variant="ghost" 
            onClick={() => setSelectedScam(null)}
            className={styles.backButton}
          >
            ← Back to Encyclopedia
          </Button>

          <div className={styles.scamDetail}>
            <div className={styles.scamHeader}>
              <div className={styles.scamIcon}>{scam.icon}</div>
              <div>
                <h1 className={styles.scamTitle}>{scam.title}</h1>
                <div className={styles.scamMeta}>
                  <Badge variant="default">{scam.category}</Badge>
                  <Badge variant={
                    scam.severity === 'Critical' ? 'danger' :
                    scam.severity === 'High' ? 'warning' : 'info'
                  }>
                    {scam.severity} Risk
                  </Badge>
                </div>
              </div>
            </div>

            <Card variant="gradient" padding="large" className={styles.tldrCard}>
              <h3 className={styles.sectionTitle}>⚡ TL;DR</h3>
              <p className={styles.tldr}>{scam.tldr}</p>
            </Card>

            <Card variant="glass" padding="large">
              <h3 className={styles.sectionTitle}>📖 Description</h3>
              <p className={styles.description}>{scam.description}</p>
            </Card>

            <Card variant="glass" padding="large">
              <h3 className={styles.sectionTitle}>⚙️ How It Works</h3>
              <ol className={styles.orderedList}>
                {scam.howItWorks.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ol>
            </Card>

            <Card variant="glass" padding="large">
              <h3 className={styles.sectionTitle}>💡 Real-World Examples</h3>
              <ul className={styles.examplesList}>
                {scam.examples.map((example, index) => (
                  <li key={index}>{example}</li>
                ))}
              </ul>
            </Card>

            <Card variant="glass" padding="large">
              <h3 className={styles.sectionTitle}>🚩 Red Flags</h3>
              <div className={styles.redFlagsGrid}>
                {scam.redFlags.map((flag, index) => (
                  <div key={index} className={styles.redFlag}>
                    <span className={styles.flagIcon}>⚠️</span>
                    <span>{flag}</span>
                  </div>
                ))}
              </div>
            </Card>

            <Card variant="glass" padding="large">
              <h3 className={styles.sectionTitle}>✅ What to Do</h3>
              <ul className={styles.actionsList}>
                {scam.whatToDo.map((action, index) => (
                  <li key={index}>{action}</li>
                ))}
              </ul>
            </Card>

            <Card variant="gradient" padding="large">
              <h3 className={styles.sectionTitle}>📊 Real-World Impact</h3>
              <p className={styles.impact}>{scam.realWorldImpact}</p>
            </Card>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className={styles.encyclopediaPage}>
        <div className={styles.header}>
          <h1 className={styles.title}>
            Scam <span className={styles.gradientText}>Encyclopedia</span>
          </h1>
          <p className={styles.subtitle}>
            Comprehensive, easy-to-understand explanations of different scam types
          </p>
        </div>

        <div className={styles.searchSection}>
          <Input 
            type="text"
            placeholder="Search scams..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            icon={<span>🔍</span>}
          />
        </div>

        <div className={styles.categoriesSection}>
          <button 
            className={`${styles.categoryChip} ${selectedCategory === 'all' ? styles.active : ''}`}
            onClick={() => setSelectedCategory('all')}
          >
            All Categories ({scamTypes.length})
          </button>
          {scamCategories.map(category => (
            <button 
              key={category.id}
              className={`${styles.categoryChip} ${selectedCategory === category.id ? styles.active : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              {category.name} ({category.count})
            </button>
          ))}
        </div>

        <div className={styles.scamsGrid}>
          {filteredScams.length === 0 ? (
            <Card variant="glass" padding="large" className={styles.noResults}>
              <div className={styles.noResultsIcon}>🔍</div>
              <h3>No Scams Found</h3>
              <p>Try adjusting your search or filter criteria</p>
            </Card>
          ) : (
            filteredScams.map(scam => (
              <Card 
                key={scam.id} 
                variant="glass" 
                hover={true}
                onClick={() => setSelectedScam(scam)}
                className={styles.scamCard}
              >
                <div className={styles.cardHeader}>
                  <div className={styles.cardIcon}>{scam.icon}</div>
                  <Badge variant={
                    scam.severity === 'Critical' ? 'danger' :
                    scam.severity === 'High' ? 'warning' : 'info'
                  }>
                    {scam.severity}
                  </Badge>
                </div>
                <h3 className={styles.cardTitle}>{scam.title}</h3>
                <p className={styles.cardCategory}>{scam.category}</p>
                <p className={styles.cardTldr}>{scam.tldr}</p>
                <Button variant="secondary" size="small" fullWidth>
                  Read More →
                </Button>
              </Card>
            ))
          )}
        </div>
      </div>
    </Layout>
  )
}

export const Head = () => <Seo title="Scam Encyclopedia - Learn About Different Scams" />

export default EncyclopediaPage
