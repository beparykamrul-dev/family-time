import React, { createContext, useContext, useState } from 'react'

const LanguageContext = createContext()

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => {
    const saved = localStorage.getItem('lang')
    return saved || 'en'
  })

  const toggleLang = () => {
    const newLang = lang === 'en' ? 'bn' : 'en'
    setLang(newLang)
    localStorage.setItem('lang', newLang)
  }

  return (
    <LanguageContext.Provider value={{ lang, toggleLang }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) throw new Error('useLanguage must be used within LanguageProvider')
  return context
}
