import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">ISP-OS Dashboard</h1>
      </nav>
      <main className="container mx-auto p-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Welcome to ISP-OS</h2>
          <p className="text-gray-600">AI-Assisted ISP Management Platform</p>
        </div>
      </main>
    </div>
  )
}

export default App
