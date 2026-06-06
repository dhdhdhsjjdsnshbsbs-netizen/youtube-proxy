from flask import Flask, jsonify, redirect
import urllib.request
import urllib.parse
import json
import os

app = Flask(__name__)

API_KEY = os.environ.get('YOUTUBE_API_KEY', '')

@app.route('/buscar/<path:termo>')
def buscar(termo):
    try:
        query = urllib.parse.quote(termo)
        url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=10&key={API_KEY}'
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode())
        musicas = []
        for item in data.get('items', []):
            titulo = item['snippet']['title']
            titulo = titulo.encode('ascii', 'ignore').decode('ascii')
            titulo = titulo.replace('"', '').replace('\\', '').replace('\n', ' ')[:50]
            musicas.append({
                'titulo': titulo,
                'id': item['id']['videoId'],
                'duracao': '0:00'
            })
        return jsonify(musicas)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/play/<video_id>')
def play(video_id):
    return redirect(f'https://www.youtube.com/watch?v={video_id}')

@app.route('/')
def index():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
