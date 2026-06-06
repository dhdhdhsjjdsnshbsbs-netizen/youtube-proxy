from flask import Flask, redirect, jsonify
import yt_dlp
import re

app = Flask(__name__)

def extrair_id(url):
    # Aceita formatos: watch?v=ID, youtu.be/ID, shorts/ID
    padrao = r'(?:v=|youtu\.be/|shorts/)([a-zA-Z0-9_-]{11})'
    resultado = re.search(padrao, url)
    if resultado:
        return resultado.group(1)
    # Se já for o ID direto (11 caracteres)
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url
    return None

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
            min = duracao // 60
            seg = duracao % 60
                musicas.append({
                    'titulo': entry.get('title', 'Sem titulo'),
                    'id': entry.get('id', ''),
                    'duracao': f'{min}:{seg:02d}'
                })
            return jsonify(musicas)
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@app.route('/')
def index():
    return jsonify({'status': 'Proxy YouTube SA-MP rodando!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
