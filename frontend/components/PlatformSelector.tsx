'use client'

interface PlatformSelectorProps {
  selectedPlatforms: string[]
  onChange: (platforms: string[]) => void
}

export default function PlatformSelector({ selectedPlatforms, onChange }: PlatformSelectorProps) {
  const platforms = [
    { id: 'youtube', name: 'YouTube', icon: '📺', enabled: true },
    // Instagram, TikTok, and Twitter are commented out - API credentials not configured
    // { id: 'instagram', name: 'Instagram', icon: '📸', enabled: false },
    // { id: 'tiktok', name: 'TikTok', icon: '🎵', enabled: false },
    // { id: 'twitter', name: 'Twitter/X', icon: '🐦', enabled: false },
  ]

  const togglePlatform = (platformId: string) => {
    if (selectedPlatforms.includes(platformId)) {
      onChange(selectedPlatforms.filter(p => p !== platformId))
    } else {
      onChange([...selectedPlatforms, platformId])
    }
  }

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">
        Select Platform (Currently YouTube Only)
      </label>
      
      <div className="grid grid-cols-1 gap-3">
        {platforms.map((platform) => (
          <button
            key={platform.id}
            type="button"
            onClick={() => platform.enabled && togglePlatform(platform.id)}
            disabled={!platform.enabled}
            className={`
              flex items-center gap-3 p-4 rounded-lg border-2 transition-all
              ${selectedPlatforms.includes(platform.id)
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 bg-white'
              }
              ${platform.enabled
                ? 'hover:border-primary-300 cursor-pointer'
                : 'opacity-50 cursor-not-allowed'
              }
            `}
          >
            <span className="text-2xl">{platform.icon}</span>
            <div className="flex-1 text-left">
              <div className="font-medium">{platform.name}</div>
              {!platform.enabled && (
                <div className="text-xs text-gray-500">Coming soon - API not configured</div>
              )}
            </div>
            {selectedPlatforms.includes(platform.id) && (
              <span className="text-primary-600">✓</span>
            )}
          </button>
        ))}
      </div>

      {selectedPlatforms.length === 0 && (
        <p className="text-sm text-gray-500 mt-2">
          Please select YouTube to continue
        </p>
      )}
    </div>
  )
}
