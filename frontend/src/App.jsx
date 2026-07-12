import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './context/ThemeContext'
import { LanguageProvider } from './context/LanguageContext'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Sidebar from './components/Sidebar'

// Pages
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Customers from './pages/Customers'
import Invoices from './pages/Invoices'
import OLTs from './pages/OLTs'
import Devices from './pages/Devices'

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              {/* Login Route */}
              <Route path="/login" element={<Login />} />

              {/* Protected Routes */}
              <Route
                path="/*"
                element={
                  <ProtectedRoute>
                    <div className="flex">
                      <Sidebar />
                      <main className="flex-1 md:ml-64 p-4 md:p-8 bg-gray-50 dark:bg-gray-900 min-h-screen">
                        <Routes>
                          <Route path="/dashboard" element={<Dashboard />} />
                          <Route path="/customers" element={<Customers />} />
                          <Route path="/invoices" element={<Invoices />} />
                          <Route path="/olts" element={<OLTs />} />
                          <Route path="/devices" element={<Devices />} />
                          <Route path="/" element={<Navigate to="/dashboard" replace />} />
                        </Routes>
                      </main>
                    </div>
                  </ProtectedRoute>
                }
              />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </LanguageProvider>
    </ThemeProvider>
  )
}

export default App
