from flask import Flask, jsonify
import asyncio
from parser import ObHavoClient
from asgiref.wsgi import WsgiToAsgi  # Flask’ni ASGI ga o‘rash uchun
from flask_cors import CORS  # 🔥 CORS qo‘shish

app = Flask(__name__)

# 🔓 CORS ni yoqamiz (hozircha barcha domenlarga ruxsat beradi)
# Agar xavfsizroq qilishni istasangiz, origins=["https://sizning-saytingiz.netlify.app"] qilib o‘zgartiring
CORS(app)

@app.route("/api/v1/obhavo/<city_name>", methods=["GET"])
def get_weather(city_name):
    """Foydalanuvchidan shahar nomini olib, ob-havo JSON natijasini qaytaradi."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(ObHavoClient(city_name).get_weather())
        loop.close()

        return jsonify({
            "status": "success",
            "city": city_name,
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# Flask ilovasini ASGI formatga o‘ramiz
asgi_app = WsgiToAsgi(app)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Uvicorn orqali ishga tushmoqda: http://127.0.0.1:8000")
    uvicorn.run("app:asgi_app", host="0.0.0.0", port=8000, reload=True)
