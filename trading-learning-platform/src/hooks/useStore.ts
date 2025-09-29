import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, UserProgress, Lesson, Achievement, Notification, AppState } from '../types';

interface StoreState extends AppState {
  // Actions
  setUser: (user: User | null) => void;
  updateProgress: (progress: Partial<UserProgress>) => void;
  setCurrentLesson: (lesson: Lesson | null) => void;
  toggleDarkMode: () => void;
  setSidebarOpen: (open: boolean) => void;
  addNotification: (notification: Omit<Notification, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  markNotificationRead: (id: string) => void;
  completeLesson: (lessonId: string) => void;
  unlockAchievement: (achievementId: string) => void;
  updateQuizScore: (quizId: string, score: number) => void;
  incrementStreak: () => void;
  resetStreak: () => void;
}

const initialProgress: UserProgress = {
  totalXP: 0,
  currentStreak: 0,
  completedLessons: [],
  achievements: [],
  quizScores: {},
  lastActive: new Date(),
  preferredLearningPath: 'both',
  currentModule: 'fundamentals',
  currentLesson: 'trading-vs-investing',
};

export const useStore = create<StoreState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      progress: initialProgress,
      currentLesson: null,
      isDarkMode: false,
      sidebarOpen: false,
      notifications: [],

      // Actions
      setUser: (user) => set({ user }),

      updateProgress: (progressUpdate) =>
        set((state) => ({
          progress: { ...state.progress, ...progressUpdate, lastActive: new Date() },
        })),

      setCurrentLesson: (lesson) => set({ currentLesson: lesson }),

      toggleDarkMode: () =>
        set((state) => {
          const newMode = !state.isDarkMode;
          // Apply dark mode class to document
          if (typeof document !== 'undefined') {
            document.documentElement.classList.toggle('dark', newMode);
          }
          return { isDarkMode: newMode };
        }),

      setSidebarOpen: (open) => set({ sidebarOpen: open }),

      addNotification: (notification) =>
        set((state) => ({
          notifications: [
            ...state.notifications,
            {
              ...notification,
              id: Date.now().toString(),
              timestamp: new Date(),
              isRead: false,
            },
          ],
        })),

      removeNotification: (id) =>
        set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== id),
        })),

      markNotificationRead: (id) =>
        set((state) => ({
          notifications: state.notifications.map((n) =>
            n.id === id ? { ...n, isRead: true } : n
          ),
        })),

      completeLesson: (lessonId) =>
        set((state) => {
          const { progress } = state;
          if (progress.completedLessons.includes(lessonId)) {
            return state; // Already completed
          }

          const newProgress = {
            ...progress,
            completedLessons: [...progress.completedLessons, lessonId],
            totalXP: progress.totalXP + 100, // Base XP for lesson completion
          };

          return { progress: newProgress };
        }),

      unlockAchievement: (achievementId) =>
        set((state) => {
          const { progress } = state;
          if (progress.achievements.includes(achievementId)) {
            return state; // Already unlocked
          }

          const newProgress = {
            ...progress,
            achievements: [...progress.achievements, achievementId],
            totalXP: progress.totalXP + 200, // Achievement bonus XP
          };

          return { progress: newProgress };
        }),

      updateQuizScore: (quizId, score) =>
        set((state) => ({
          progress: {
            ...state.progress,
            quizScores: { ...state.progress.quizScores, [quizId]: score },
            totalXP: state.progress.totalXP + Math.floor(score / 10), // XP based on score
          },
        })),

      incrementStreak: () =>
        set((state) => ({
          progress: {
            ...state.progress,
            currentStreak: state.progress.currentStreak + 1,
            totalXP: state.progress.totalXP + 50, // Streak bonus XP
          },
        })),

      resetStreak: () =>
        set((state) => ({
          progress: { ...state.progress, currentStreak: 0 },
        })),
    }),
    {
      name: 'trading-platform-storage',
      partialize: (state) => ({
        user: state.user,
        progress: state.progress,
        isDarkMode: state.isDarkMode,
      }),
    }
  )
);

// Helper hooks for specific parts of state
export const useUser = () => useStore((state) => state.user);
export const useProgress = () => useStore((state) => state.progress);
export const useCurrentLesson = () => useStore((state) => state.currentLesson);
export const useDarkMode = () => useStore((state) => state.isDarkMode);
export const useNotifications = () => useStore((state) => state.notifications);