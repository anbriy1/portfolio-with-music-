from flask import Flask, jsonify
import traceback

# Твой токен
TOKEN = ""

app = Flask(__name__)

def get_current_track_data():
    try:
        from yandex_music import Client
        client = Client(TOKEN)
        client.init()

        queues = client.queues_list()
        if not queues or len(queues) == 0:
            return {"error": "Нет активных очередей"}, 404

        queue = queues[0]
        track = queue.get_current_track()
        if not track:
            return {"error": "Музыка не воспроизводится"}, 404

        artists = ', '.join([artist.name for artist in track.artists])
        cover_url = f"https://{track.cover_uri.replace('%%', '400x400')}" if track.cover_uri else None
        duration_sec = track.duration_ms / 1000 if hasattr(track, 'duration_ms') else 0
        minutes = int(duration_sec // 60)
        seconds = int(duration_sec % 60)

        return {
            "title": track.title,
            "artists": artists,
            "album": track.albums[0].title if track.albums else None,
            "cover": cover_url,
            "duration": f"{minutes}:{seconds:02d}"
        }

    except ImportError:
        return {"error": "Библиотека yandex-music не установлена"}, 500
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}, 500

@app.route("/current_track")
def api_current_track():
    data, status = get_current_track_data(), 200
    if "error" in data:
        status = data.get("status", 500)
    return jsonify(data), status

if __name__ == "__main__":
    app.run(debug=True)