import React from 'react'

function StatsCard({ title, value, subtitle, color = 'blue', icon: Icon }) {
  const colorMap = {
    blue: 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400',
    green: 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400',
    red: 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400',
    yellow: 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400',
    gray: 'bg-gray-50 dark:bg-gray-700 text-gray-700 dark:text-gray-300',
  }

  return (
    <div className="p-4 rounded-lg shadow-sm bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:shadow-md transition">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
          <p className="text-2xl font-bold mt-1 text-gray-900 dark:text-white">{value}</p>
          {subtitle && <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-3 rounded-md ${colorMap[color] || colorMap.blue}`}>
          {Icon ? <Icon className="w-6 h-6" /> : null}
        </div>
      </div>
    </div>
  )
}

export default StatsCard
