import React, { useEffect, useState } from 'react'
import { useLanguage } from '../context/LanguageContext'
import { useTheme } from '../context/ThemeContext'
import translations from '../i18n/translations'
import StatsCard from '../components/StatsCard'
import RevenueChart from '../components/RevenueChart'
import NetworkMap from '../components/NetworkMap'
import AlertsPanel from '../components/AlertsPanel'
import ThemeToggle from '../components/ThemeToggle'
import LanguageToggle from '../components/LanguageToggle'
import { Server, Users, Cpu, AlertCircle } from 'lucide-react'
import mock from '../mock/dashboard.json'
import axios from 'axios'

function Dashboard() {
  const [data, setData] = useState(mock)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const { lang } = useLanguage()
  const { isDark } = useTheme()
  const t = translations[lang]

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    setLoading(true)
    setError(null)
    try {
      // Try to fetch from API first
      const response = await axios.get('http://localhost:8000/api/dashboard', {
        timeout: 5000,
      })
      setData(response.data)
    } catch (err) {
      console.warn('API not available, using mock data:', err.message)
      // Fall back to mock data if API is not available
      setData(mock)
    } finally {
      setLoading(false)
    }
  }

  const refreshData = () => {
    fetchDashboardData()
  }

  return (
    <div className={`min-h-screen ${isDark ? 'dark bg-gray-900' : 'bg-gray-50'}`}>
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow border-b border-gray-200 dark:border-gray-700 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{lang === 'en' ? 'Dashboard' : 'ড্যাশবোর্ড'}</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{lang === 'en' ? 'ISP Management System' : 'ISP ম্যানেজমেন্ট সিস্টেম'}</p>
            </div>
            <div className="flex items-center gap-3">
              {loading && <span className="text-sm text-gray-500 dark:text-gray-400">⟳ Loading...</span>}
              <button
                onClick={refreshData}
                className="px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 transition text-sm font-medium"
              >
                {lang === 'en' ? '↻ Refresh' : '↻ রিফ্রেশ'}
              </button>
              <LanguageToggle />
              <ThemeToggle />
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-medium text-red-900 dark:text-red-300">{lang === 'en' ? 'Error' : 'তথ্য'}</p>
              <p className="text-sm text-red-700 dark:text-red-200">{error}</p>
            </div>
          </div>
        )}

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <StatsCard
            title={t.totalCustomers}
            value={data.stats?.totalCustomers || 0}
            subtitle={t.allTime}
            icon={Users}
            color="blue"
          />
          <StatsCard
            title={t.activeUsers}
            value={data.stats?.activeUsers || 0}
            subtitle={t.currentlyOnline}
            icon={Server}
            color="green"
          />
          <StatsCard
            title={t.monthlyRevenue}
            value={`৳${(data.stats?.monthlyRevenue || 0).toLocaleString()}`}
            subtitle={t.thisMonth}
            icon={Cpu}
            color="blue"
          />
          <StatsCard
            title={t.overdueCustomers}
            value={data.stats?.overdueCustomers || 0}
            subtitle={t.requireAttention}
            color="red"
          />
        </div>

        {/* Charts and Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
          <div className="lg:col-span-2">
            <RevenueChart data={data.revenue || []} />
          </div>
          <div className="space-y-4">
            <AlertsPanel alerts={data.alerts || []} />
            <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700">
              <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">{t.recentActivity}</h3>
              <ul className="space-y-2">
                {(data.recent || []).map((r) => (
                  <li key={r.id} className="text-sm text-gray-700 dark:text-gray-300 p-2 hover:bg-gray-50 dark:hover:bg-gray-700/50 rounded transition">
                    <span className="text-gray-500 dark:text-gray-400">{r.time}</span>
                    <br />
                    {r.title}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Network Map */}
        <div>
          <NetworkMap devices={data.devices || []} center={[23.8103, 90.4125]} zoom={12} />
        </div>
      </div>
    </div>
  )
}

export default Dashboard
