import * as React from "react"
import { useState, useEffect } from "react"
import Layout from "../components/layout"
import Seo from "../components/seo"
import { Card, Button, Badge, ProgressBar } from "../components/elements"
import { courses } from "../data/coursesData"
import StorageManager from "../utils/storageManager"
import * as styles from "./learn.module.css"

const LearnPage = () => {
  const [progress, setProgress] = useState(null)
  const [stats, setStats] = useState(null)
  const [streak, setStreak] = useState(null)

  useEffect(() => {
    // Load user data from local storage
    setProgress(StorageManager.getProgress())
    setStats(StorageManager.getStats())
    setStreak(StorageManager.getStreak())
  }, [])

  if (!progress || !stats || !streak) {
    return <Layout><div style={{ padding: '6rem 2rem', textAlign: 'center' }}>Loading...</div></Layout>
  }

  const totalLessons = courses.reduce((sum, course) => sum + course.lessons, 0)
  const completedPercentage = (progress.completedLessons.length / totalLessons) * 100
  const accuracy = stats.totalAnswers > 0 
    ? Math.round((stats.correctAnswers / stats.totalAnswers) * 100) 
    : 0

  return (
    <Layout>
      <div className={styles.learnPage}>
        {/* Header Section */}
        <div className={styles.header}>
          <h1 className={styles.title}>
            <span className={styles.gradientText}>Learn & Master</span> Phishing Prevention
          </h1>
          <p className={styles.subtitle}>
            Gamified lessons to help you identify and protect against phishing attacks
          </p>
        </div>

        {/* Stats Dashboard */}
        <div className={styles.statsGrid}>
          <Card variant="glass" padding="large">
            <div className={styles.statCard}>
              <div className={styles.statIcon}>🔥</div>
              <div>
                <div className={styles.statValue}>{streak.current} Days</div>
                <div className={styles.statLabel}>Current Streak</div>
              </div>
            </div>
          </Card>

          <Card variant="glass" padding="large">
            <div className={styles.statCard}>
              <div className={styles.statIcon}>⭐</div>
              <div>
                <div className={styles.statValue}>{progress.totalPoints}</div>
                <div className={styles.statLabel}>Total Points</div>
              </div>
            </div>
          </Card>

          <Card variant="glass" padding="large">
            <div className={styles.statCard}>
              <div className={styles.statIcon}>🎯</div>
              <div>
                <div className={styles.statValue}>{accuracy}%</div>
                <div className={styles.statLabel}>Accuracy</div>
              </div>
            </div>
          </Card>

          <Card variant="glass" padding="large">
            <div className={styles.statCard}>
              <div className={styles.statIcon}>🏆</div>
              <div>
                <div className={styles.statValue}>Level {progress.level}</div>
                <div className={styles.statLabel}>Current Level</div>
              </div>
            </div>
          </Card>
        </div>

        {/* Overall Progress */}
        <Card variant="glass" padding="large" className={styles.progressCard}>
          <h3 className={styles.sectionTitle}>Overall Progress</h3>
          <div className={styles.progressInfo}>
            <span>{progress.completedLessons.length} of {totalLessons} lessons completed</span>
            <span>{Math.round(completedPercentage)}%</span>
          </div>
          <ProgressBar 
            value={progress.completedLessons.length} 
            max={totalLessons} 
            variant="primary"
            size="large"
          />
        </Card>

        {/* Courses Grid */}
        <div className={styles.coursesSection}>
          <h2 className={styles.sectionTitle}>Available Courses</h2>
          <div className={styles.coursesGrid}>
            {courses.map((course) => {
              const completed = progress.completedLessons.filter(id => 
                id.startsWith(course.id)
              ).length
              const courseProgress = (completed / course.lessons) * 100

              return (
                <Card 
                  key={course.id} 
                  variant="glass" 
                  hover={true}
                  className={styles.courseCard}
                >
                  <div className={styles.courseIcon}>{course.icon}</div>
                  <div className={styles.courseContent}>
                    <div className={styles.courseHeader}>
                      <h3 className={styles.courseTitle}>{course.title}</h3>
                      <Badge variant={
                        course.level === 'Beginner' ? 'success' :
                        course.level === 'Intermediate' ? 'warning' : 'danger'
                      }>
                        {course.level}
                      </Badge>
                    </div>
                    <p className={styles.courseDescription}>{course.description}</p>
                    <div className={styles.courseInfo}>
                      <span>📚 {course.lessons} lessons</span>
                      <span>⏱️ {course.estimatedTime}</span>
                    </div>
                    <div className={styles.courseProgress}>
                      <ProgressBar 
                        value={completed} 
                        max={course.lessons}
                        variant="primary"
                        showLabel={true}
                        label={`${completed}/${course.lessons} completed`}
                      />
                    </div>
                    <Button 
                      fullWidth 
                      variant={courseProgress === 100 ? 'secondary' : 'primary'}
                    >
                      {courseProgress === 100 ? 'Review Course' : 
                       courseProgress > 0 ? 'Continue' : 'Start Course'}
                    </Button>
                  </div>
                </Card>
              )
            })}
          </div>
        </div>

        {/* WhatsApp Drip Content Section */}
        <Card variant="gradient" padding="large" className={styles.whatsappSection}>
          <div className={styles.whatsappContent}>
            <div className={styles.whatsappIcon}>💬</div>
            <div>
              <h3 className={styles.whatsappTitle}>Get Daily Tips on WhatsApp</h3>
              <p className={styles.whatsappDescription}>
                Receive bite-sized security awareness content daily. No login required!
              </p>
            </div>
            <Button variant="primary" size="large">
              Subscribe via WhatsApp
            </Button>
          </div>
        </Card>
      </div>
    </Layout>
  )
}

export const Head = () => <Seo title="Learn - Gamified Phishing Training" />

export default LearnPage
