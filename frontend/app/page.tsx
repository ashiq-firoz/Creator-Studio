'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-primary-600">Creator Dashboard</h1>
            </div>
            <div className="flex gap-4">
              <Link href="/login" className="text-gray-700 hover:text-primary-600">
                Login
              </Link>
              <Link href="/register" className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Automate Your Content Creation Workflow
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
            Upload once, distribute everywhere. AI-powered platform for content adaptation,
            multi-platform distribution, and intelligent monetization.
          </p>

          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white p-8 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">🎬</div>
              <h3 className="text-xl font-bold mb-3">One-Click Adaptation</h3>
              <p className="text-gray-600">
                Automatically adapt your content for YouTube, Instagram, TikTok, and Twitter
                with AI-generated titles, descriptions, and thumbnails.
              </p>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">🚀</div>
              <h3 className="text-xl font-bold mb-3">Unified Distribution</h3>
              <p className="text-gray-600">
                Schedule or publish instantly across all platforms simultaneously.
                Track performance in real-time from one dashboard.
              </p>
            </div>

            <div className="bg-white p-8 rounded-xl shadow-lg">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-bold mb-3">Smart Monetization</h3>
              <p className="text-gray-600">
                AI-powered ad placement that naturally integrates with your content
                without disrupting viewer experience.
              </p>
            </div>
          </div>

          <div className="mt-16">
            <Link 
              href="/dashboard" 
              className="bg-primary-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-primary-700 inline-block"
            >
              Launch Dashboard
            </Link>
          </div>
        </div>
      </main>
    </div>
  )
}
