// Local Storage Manager for Awareness Training
const STORAGE_KEYS = {
  USER_PROGRESS: 'phishguard_user_progress',
  COMPLETED_LESSONS: 'phishguard_completed_lessons',
  USER_STATS: 'phishguard_user_stats',
  STREAK: 'phishguard_streak',
  LAST_VISIT: 'phishguard_last_visit',
};

export const StorageManager = {
  // Get user progress
  getProgress: () => {
    if (typeof window === 'undefined') return null;
    const data = localStorage.getItem(STORAGE_KEYS.USER_PROGRESS);
    return data ? JSON.parse(data) : {
      totalPoints: 0,
      level: 1,
      completedLessons: [],
      currentCourse: null,
    };
  },

  // Save user progress
  saveProgress: (progress) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(STORAGE_KEYS.USER_PROGRESS, JSON.stringify(progress));
  },

  // Get user stats
  getStats: () => {
    if (typeof window === 'undefined') return null;
    const data = localStorage.getItem(STORAGE_KEYS.USER_STATS);
    return data ? JSON.parse(data) : {
      lessonsCompleted: 0,
      correctAnswers: 0,
      totalAnswers: 0,
      timeSpent: 0,
      achievements: [],
    };
  },

  // Save user stats
  saveStats: (stats) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(STORAGE_KEYS.USER_STATS, JSON.stringify(stats));
  },

  // Get streak data
  getStreak: () => {
    if (typeof window === 'undefined') return null;
    const data = localStorage.getItem(STORAGE_KEYS.STREAK);
    return data ? JSON.parse(data) : {
      current: 0,
      longest: 0,
      lastDate: null,
    };
  },

  // Update streak
  updateStreak: () => {
    if (typeof window === 'undefined') return;
    const streak = StorageManager.getStreak();
    const today = new Date().toDateString();
    const lastDate = streak.lastDate;

    if (lastDate === today) {
      return streak; // Already counted today
    }

    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const yesterdayStr = yesterday.toDateString();

    if (lastDate === yesterdayStr) {
      // Continue streak
      streak.current += 1;
      streak.longest = Math.max(streak.longest, streak.current);
    } else if (lastDate !== today) {
      // Reset streak if missed a day
      streak.current = 1;
    }

    streak.lastDate = today;
    localStorage.setItem(STORAGE_KEYS.STREAK, JSON.stringify(streak));
    return streak;
  },

  // Complete a lesson
  completeLesson: (lessonId, points, correctAnswers, totalAnswers) => {
    if (typeof window === 'undefined') return;
    
    const progress = StorageManager.getProgress();
    const stats = StorageManager.getStats();
    const streak = StorageManager.updateStreak();

    if (!progress.completedLessons.includes(lessonId)) {
      progress.completedLessons.push(lessonId);
      progress.totalPoints += points;
      
      // Level up logic (every 100 points)
      progress.level = Math.floor(progress.totalPoints / 100) + 1;
    }

    stats.lessonsCompleted += 1;
    stats.correctAnswers += correctAnswers;
    stats.totalAnswers += totalAnswers;

    StorageManager.saveProgress(progress);
    StorageManager.saveStats(stats);

    return { progress, stats, streak };
  },

  // Check if lesson is completed
  isLessonCompleted: (lessonId) => {
    if (typeof window === 'undefined') return false;
    const progress = StorageManager.getProgress();
    return progress.completedLessons.includes(lessonId);
  },

  // Add achievement
  addAchievement: (achievement) => {
    if (typeof window === 'undefined') return;
    const stats = StorageManager.getStats();
    if (!stats.achievements.find(a => a.id === achievement.id)) {
      stats.achievements.push({
        ...achievement,
        unlockedAt: new Date().toISOString(),
      });
      StorageManager.saveStats(stats);
    }
  },

  // Clear all data (for testing)
  clearAll: () => {
    if (typeof window === 'undefined') return;
    Object.values(STORAGE_KEYS).forEach(key => {
      localStorage.removeItem(key);
    });
  },
};

export default StorageManager;
