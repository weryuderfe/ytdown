import React, { useState } from 'react';
import { Download, Youtube, Music, Video, Settings, X } from 'lucide-react';

type Format = 'mp3' | 'mp4';
type Quality = 'low' | 'medium' | 'high' | 'best';

interface DownloadOptions {
  format: Format;
  quality: Quality;
  url: string;
}

function App() {
  const [url, setUrl] = useState('');
  const [format, setFormat] = useState<Format>('mp4');
  const [quality, setQuality] = useState<Quality>('high');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [downloadHistory, setDownloadHistory] = useState<DownloadOptions[]>([]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
      setError('Please enter a valid YouTube URL');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, format, quality }),
      });

      if (!response.ok) {
        throw new Error('Download failed');
      }

      setDownloadHistory(prev => [...prev, { url, format, quality }]);
      setUrl('');
    } catch (err) {
      setError('Failed to download. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center mb-8">
          <Youtube className="w-12 h-12 text-red-500 mr-4" />
          <h1 className="text-4xl font-bold">YouTube Downloader</h1>
        </div>

        <div className="max-w-2xl mx-auto bg-gray-800 rounded-lg shadow-xl p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">YouTube URL</label>
              <div className="relative">
                <input
                  type="text"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="w-full bg-gray-700 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                />
                {url && (
                  <button
                    type="button"
                    onClick={() => setUrl('')}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    <X className="w-5 h-5" />
                  </button>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Format</label>
                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={() => setFormat('mp4')}
                    className={`flex items-center px-4 py-2 rounded-lg ${
                      format === 'mp4'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    <Video className="w-5 h-5 mr-2" />
                    MP4
                  </button>
                  <button
                    type="button"
                    onClick={() => setFormat('mp3')}
                    className={`flex items-center px-4 py-2 rounded-lg ${
                      format === 'mp3'
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                    }`}
                  >
                    <Music className="w-5 h-5 mr-2" />
                    MP3
                  </button>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Quality</label>
                <select
                  value={quality}
                  onChange={(e) => setQuality(e.target.value as Quality)}
                  className="w-full bg-gray-700 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="best">Best</option>
                </select>
              </div>
            </div>

            {error && (
              <div className="bg-red-500/20 text-red-400 px-4 py-2 rounded-lg">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || !url}
              className={`w-full flex items-center justify-center px-6 py-3 rounded-lg text-lg font-medium ${
                isLoading || !url
                  ? 'bg-gray-600 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700'
              }`}
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white" />
              ) : (
                <>
                  <Download className="w-6 h-6 mr-2" />
                  Download
                </>
              )}
            </button>
          </form>

          {downloadHistory.length > 0 && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4 flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                Download History
              </h2>
              <div className="space-y-2">
                {downloadHistory.map((item, index) => (
                  <div
                    key={index}
                    className="bg-gray-700 rounded-lg p-3 flex items-center justify-between"
                  >
                    <div className="flex items-center">
                      {item.format === 'mp4' ? (
                        <Video className="w-5 h-5 mr-2 text-blue-400" />
                      ) : (
                        <Music className="w-5 h-5 mr-2 text-green-400" />
                      )}
                      <span className="truncate max-w-md">{item.url}</span>
                    </div>
                    <span className="text-sm bg-gray-600 px-2 py-1 rounded">
                      {item.format.toUpperCase()} - {item.quality}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;