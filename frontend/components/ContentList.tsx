'use client'

interface Content {
  id: string
  title: string
  description: string
  upload_status: string
  created_at: string
}

interface ContentListProps {
  content: Content[]
  isLoading: boolean
}

export default function ContentList({ content, isLoading }: ContentListProps) {
  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading content...</p>
      </div>
    )
  }

  if (!content || content.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📁</div>
        <h3 className="text-xl font-semibold mb-2">No content yet</h3>
        <p className="text-gray-600">Upload your first video to get started</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold mb-4">Your Content</h2>
      
      <div className="grid gap-4">
        {content.map((item) => (
          <div
            key={item.id}
            className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-1">{item.title}</h3>
                <p className="text-gray-600 text-sm mb-2">{item.description}</p>
                <div className="flex gap-4 text-sm text-gray-500">
                  <span>Status: {item.upload_status}</span>
                  <span>Created: {new Date(item.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              
              <div className="flex gap-2">
                <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 text-sm">
                  Distribute
                </button>
                <button className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm">
                  View
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
