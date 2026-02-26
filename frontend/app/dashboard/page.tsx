'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { contentAPI } from '@/lib/api'
import UploadSection from '@/components/UploadSection'
import ContentList from '@/components/ContentList'

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('upload')

  const { data: contentData, isLoading } = useQuery({
    queryKey: ['content'],
    queryFn: () => contentAPI.listContent(),
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-2xl font-bold text-primary-600">Creator Dashboard</h1>
            <div className="flex gap-4">
              <button className="text-gray-700 hover:text-primary-600">
                Profile
              </button>
              <button className="text-gray-700 hover:text-primary-600">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              {['upload', 'content', 'analytics', 'monetization'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`${
                    activeTab === tab
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm capitalize`}
                >
                  {tab}
                </button>
              ))}
            </nav>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          {activeTab === 'upload' && <UploadSection />}
          {activeTab === 'content' && (
            <ContentList content={contentData?.data?.content || []} isLoading={isLoading} />
          )}
          {activeTab === 'analytics' && (
            <div className="text-center py-12">
              <h3 className="text-xl font-semibold mb-2">Analytics Dashboard</h3>
              <p className="text-gray-600">View performance metrics across all platforms</p>
            </div>
          )}
          {activeTab === 'monetization' && (
            <div className="text-center py-12">
              <h3 className="text-xl font-semibold mb-2">Monetization</h3>
              <p className="text-gray-600">Manage ad placements and revenue</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
