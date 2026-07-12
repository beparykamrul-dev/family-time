import React from 'react'

function AlertsPanel({ alerts = [] }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Alerts</h3>
      <div className="space-y-2 max-h-72 overflow-y-auto">
        {alerts.length === 0 && <p className="text-sm text-gray-500 dark:text-gray-400">No alerts</p>}
        {alerts.map((a) => (
          <div key={a.id} className="flex items-start gap-3 p-3 border rounded-md dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition">
            <div className={`w-3 h-3 rounded-full mt-1 flex-shrink-0 ${a.severity === 'critical' ? 'bg-red-500' : a.severity === 'warning' ? 'bg-yellow-500' : 'bg-green-500'}`}></div>
            <div className="flex-1">
              <div className="text-sm font-medium text-gray-900 dark:text-white">{a.title}</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">{a.time}</div>
              <div className="text-sm text-gray-700 dark:text-gray-300 mt-1">{a.details}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AlertsPanel
