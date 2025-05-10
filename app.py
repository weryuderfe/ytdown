from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from downloader import YouTubeDownloader
from utils import validate_url, create_output_dir

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Create downloads directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
create_output_dir(DOWNLOAD_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        url = data.get('url')
        format_type = data.get('format', 'mp4')
        quality = data.get('quality', 'high')

        if not url or not validate_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400

        downloader = YouTubeDownloader(
            url=url,
            format_type=format_type,
            output_dir=DOWNLOAD_DIR,
            quality=quality
        )

        success = downloader.download()
        
        if success:
            return jsonify({'message': 'Download completed successfully'})
        else:
            return jsonify({'error': 'Download failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)