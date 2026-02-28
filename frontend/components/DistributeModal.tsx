'use client'

import { useState } from 'react'
import PlatformSelector from './PlatformSelector'
import { distributionAPI } from '@/lib/api'

interface DistributeModalProps {
  contentId: string
  onClose: () => void
  onSuccess: () => void
}

export default function DistributeModal({ contentId, onClose, onSuccess }: DistributeModalProps) {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['youtube'])
  const [isScheduled, setIsScheduled] = useState(false)
  const [scheduledTime, setScheduledTime] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (selectedPlatforms.length === 0) {
      setError('Please select YouTube')
      return
    }

    setIsSubmitting(true)

    try {
      await distributionAPI.distribute({
        content_id: contentId,
        platforms: selectedPlatforms,
        scheduled_time: isScheduled ? scheduledTime : undefined,
        immediate: !isScheduled,
      })

      onSuccess()
      onClose()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to distribute content')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Distribute Content</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <PlatformSelector
            selectedPlatforms={selectedPlatforms}
            onChange={setSelectedPlatforms}
          />

          <div className="space-y-2">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={isScheduled}
                onChange={(e) => setIsScheduled(e.target.checked)}
                className="rounded"
              />
              <span className="text-sm font-medium">Schedule for later</span>
            </label>

            {isScheduled && (
              <input
                type="datetime-local"
                value={scheduledTime}
                onChange={(e) => setScheduledTime(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                required
              />
            )}
          </div>

          {error && (
            <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting || selectedPlatforms.length === 0}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Publishing...' : isScheduled ? 'Schedule' : 'Publish Now'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
