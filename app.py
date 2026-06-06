from flask import Flask, jsonify, redirect
import yt_dlp
import re
import os

app = Flask(__name__)

@app.route('/play/<video_id>')
def play(video_id):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f'https://youtube.com/watch?v={video_id}', download=False)
            url = info['url']
            return redirect(url)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/buscar/<path:termo>')
def buscar(termo):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            resultado = ydl.extract_info(f'ytsearch5:{termo}', download=False)
            musicas = []
            for entry in resultado['entries']:
                duracao = int(entry.get('duration', 0) or 0)
                m = duracao // 60
                s = duracao % 60
                # Remove caracteres especiais do titulo para evitar quebrar o parser
                titulo = entry.get('title', 'Sem titulo')
                titulo = titulo.encode('ascii', 'ignore').decode('ascii')
                titulo = titulo.replace('"', '').replace('\\', '').replace('\n', ' ')[:50]
                musicas.append({
                    'titulo': titulo,
                    'id': entry.get('id', ''),
                    'duracao': f'{m}:{s:02d}'
                })
            return jsonify(musicas)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/')
def index():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
