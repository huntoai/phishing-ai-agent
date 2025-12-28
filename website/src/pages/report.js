import * as React from "react"
import { useState } from "react"
import Layout from "../components/layout"
import Seo from "../components/seo"
import { Card, Button, Input, Badge } from "../components/elements"
import * as styles from "./report.module.css"

const ReportPage = () => {
  const [formData, setFormData] = useState({
    type: '',
    description: '',
    url: '',
    email: '',
    phone: '',
  })
  const [submitted, setSubmitted] = useState(false)
  const [reportId, setReportId] = useState(null)

  const handleSubmit = (e) => {
    e.preventDefault()
    // Generate mock report ID
    const id = 'SCAM-' + Math.random().toString(36).substr(2, 9).toUpperCase()
    setReportId(id)
    setSubmitted(true)
    
    // In production, this would call the API
    // Store in localStorage for now
    const reports = JSON.parse(localStorage.getItem('phishguard_reports') || '[]')
    reports.push({
      id,
      ...formData,
      date: new Date().toISOString(),
      status: 'pending'
    })
    localStorage.setItem('phishguard_reports', JSON.stringify(reports))
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const guidanceResources = [
    {
      title: 'Federal Trade Commission (FTC)',
      url: 'https://reportfraud.ftc.gov',
      description: 'Report identity theft and fraud',
      icon: '🏛️'
    },
    {
      title: 'FBI Internet Crime Complaint Center',
      url: 'https://www.ic3.gov',
      description: 'Report internet-facilitated crimes',
      icon: '🔍'
    },
    {
      title: 'Your Bank\'s Fraud Department',
      description: 'Contact immediately if financial information was compromised',
      icon: '🏦'
    },
    {
      title: 'Local Police',
      description: 'File a report if you lost money or your identity was stolen',
      icon: '👮'
    },
  ]

  const nextSteps = [
    { step: 1, title: 'Change Passwords', description: 'If you shared any passwords, change them immediately' },
    { step: 2, title: 'Monitor Accounts', description: 'Check bank and credit card statements regularly' },
    { step: 3, title: 'Enable 2FA', description: 'Add two-factor authentication to your accounts' },
    { step: 4, title: 'Credit Monitoring', description: 'Consider placing a fraud alert on your credit reports' },
    { step: 5, title: 'Document Everything', description: 'Save all evidence including emails, messages, and screenshots' },
  ]

  if (submitted) {
    return (
      <Layout>
        <div className={styles.reportPage}>
          <Card variant="glass" padding="large" className={styles.successCard}>
            <div className={styles.successIcon}>✅</div>
            <h2 className={styles.successTitle}>Report Submitted Successfully</h2>
            <p className={styles.successMessage}>
              Your report has been submitted and will be reviewed by our team.
            </p>
            <div className={styles.reportIdBox}>
              <div className={styles.reportIdLabel}>Your Report ID:</div>
              <div className={styles.reportId}>{reportId}</div>
              <div className={styles.reportIdNote}>
                Save this ID to check the status of your report
              </div>
            </div>
            
            <Button onClick={() => setSubmitted(false)} variant="secondary">
              Submit Another Report
            </Button>
          </Card>

          <div className={styles.guidanceSection}>
            <h3 className={styles.sectionTitle}>What to Do Next</h3>
            
            <div className={styles.nextStepsGrid}>
              {nextSteps.map((item) => (
                <Card key={item.step} variant="glass" padding="medium">
                  <div className={styles.stepNumber}>{item.step}</div>
                  <h4 className={styles.stepTitle}>{item.title}</h4>
                  <p className={styles.stepDescription}>{item.description}</p>
                </Card>
              ))}
            </div>

            <h3 className={styles.sectionTitle} style={{ marginTop: '3rem' }}>
              Report to Authorities
            </h3>
            <div className={styles.resourcesGrid}>
              {guidanceResources.map((resource, index) => (
                <Card key={index} variant="glass" padding="large" hover={true}>
                  <div className={styles.resourceIcon}>{resource.icon}</div>
                  <h4 className={styles.resourceTitle}>{resource.title}</h4>
                  <p className={styles.resourceDescription}>{resource.description}</p>
                  {resource.url && (
                    <a href={resource.url} target="_blank" rel="noopener noreferrer">
                      <Button variant="secondary" size="small" fullWidth>
                        Visit Website
                      </Button>
                    </a>
                  )}
                </Card>
              ))}
            </div>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className={styles.reportPage}>
        <div className={styles.header}>
          <h1 className={styles.title}>
            Report a <span className={styles.gradientText}>Phishing Scam</span>
          </h1>
          <p className={styles.subtitle}>
            Help us protect others by reporting suspicious activity. We'll review your report and provide guidance on next steps.
          </p>
        </div>

        <div className={styles.formContainer}>
          <Card variant="glass" padding="large">
            <form onSubmit={handleSubmit} className={styles.form}>
              <div className={styles.formGroup}>
                <label className={styles.label}>Type of Scam *</label>
                <select 
                  name="type"
                  className={styles.select}
                  value={formData.type}
                  onChange={handleChange}
                  required
                >
                  <option value="">Select type...</option>
                  <option value="email">Email Phishing</option>
                  <option value="sms">SMS/Smishing</option>
                  <option value="phone">Phone/Vishing</option>
                  <option value="social">Social Media</option>
                  <option value="website">Fake Website</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>Description *</label>
                <textarea 
                  name="description"
                  className={styles.textarea}
                  placeholder="Describe what happened..."
                  value={formData.description}
                  onChange={handleChange}
                  required
                  rows={5}
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>Suspicious URL or Link</label>
                <Input 
                  type="text"
                  name="url"
                  placeholder="https://example.com"
                  value={formData.url}
                  onChange={handleChange}
                />
              </div>

              <div className={styles.formRow}>
                <div className={styles.formGroup}>
                  <label className={styles.label}>Sender Email (if applicable)</label>
                  <Input 
                    type="email"
                    name="email"
                    placeholder="scammer@example.com"
                    value={formData.email}
                    onChange={handleChange}
                  />
                </div>

                <div className={styles.formGroup}>
                  <label className={styles.label}>Sender Phone (if applicable)</label>
                  <Input 
                    type="tel"
                    name="phone"
                    placeholder="+1 (555) 123-4567"
                    value={formData.phone}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <div className={styles.submitSection}>
                <Button type="submit" size="large" fullWidth>
                  Submit Report
                </Button>
              </div>
            </form>
          </Card>

          <Card variant="gradient" padding="large" className={styles.infoCard}>
            <h3 className={styles.infoTitle}>📋 What Happens Next?</h3>
            <ul className={styles.infoList}>
              <li>Your report will be reviewed by our security team</li>
              <li>We'll add it to our database to protect others</li>
              <li>You'll receive guidance on how to protect yourself</li>
              <li>Your information is kept confidential</li>
            </ul>
          </Card>
        </div>
      </div>
    </Layout>
  )
}

export const Head = () => <Seo title="Report a Scam - PhishGuard" />

export default ReportPage
