import React from 'react'
import { useLanguage } from '../context/LanguageContext'
import translations from '../i18n/translations'

function LanguageToggle() {
  const { lang, toggleLang } = useLanguage()
  const t = translations[lang]

  return (
    <button
      onClick={toggleLang}
      className="px-3 py-2 rounded-lg bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 font-medium hover:bg-blue-200 dark:hover:bg-blue-800 transition text-sm"
      title={t.language}
    >
      {lang === 'en' ? '🇧🇩 বাংলা' : '🇬🇧 English'}
    </button>
  )
}

export default LanguageToggle
