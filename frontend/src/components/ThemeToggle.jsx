import React from 'react'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'
import { useLanguage } from '../context/LanguageContext'
import translations from '../i18n/translations'

function ThemeToggle() {
  const { isDark, toggleDark } = useTheme()
  const { lang } = useLanguage()
  const t = translations[lang]

  return (
    <button
      onClick={toggleDark}
      className="p-2 rounded-lg bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition"
      title={t.darkMode}
    >
      {isDark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
    </button>
  )
}

export default ThemeToggle
