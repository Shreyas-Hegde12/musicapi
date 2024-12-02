from flask import Flask, request, render_template, jsonify
from musicapi import get_song_recommendation, continue_recommendation
from yt_dlp import YoutubeDL

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return render_template('3.html')

@app.route('/getsongs', methods=['POST'])
def getsongs():
    data = request.get_json()
    if not data or 'emotion' not in data:
        return jsonify({'error': 'Emotion is required'}), 400
    emotion = data['emotion']
    try:
        music_json = get_song_recommendation(emotion)
        return jsonify(music_json), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    

@app.route('/continuesongs', methods=['POST'])
def continuesongs():
    data = request.get_json()
    if not data or 'videoid' not in data:
        return jsonify({'error': 'videoid is required'}), 400
    vidid = data['videoid']
    try:
        musicnext_json = continue_recommendation(vidid)
        return jsonify(musicnext_json), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    
@app.route('/songurl', methods=['POST'])
def songurl():
    data = request.get_json()
    if not data or 'videoid' not in data:
        return jsonify({'error': 'videoid is required'}), 400
    videoid = data['videoid']
    try:
        ydl_opts = {
            'format': 'bestaudio/best',  # Best quality audio format
            'noplaylist': True,
            'quiet': True,
            'simulate': True,  # No actual download
            'forceurl': True,  # Output only the direct URL
        }
        song_url =''
        with YoutubeDL(ydl_opts) as ydl:
            song_url = ydl.extract_info(f'https://youtube.com/watch?v={videoid}', download=False)
        song_url = song_url['url']

        return jsonify({'songurl':song_url}), 200
    except Exception as e:
        return jsonify({'error':str(e)}), 500
    


if __name__=="__main__":
    app.run(debug=True)

