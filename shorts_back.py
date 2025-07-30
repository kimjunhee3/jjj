from flask import Flask, render_template
from shorts import fetch_kbo_shorts
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
        shorts = fetch_kbo_shorts()  # ✅ 실시간 크롤링 수행
    except Exception as e:
        print(f"❌ 크롤링 에러 발생: {e}")
        shorts = []  # 에러 발생 시 빈 리스트 전달
    return render_template("shorts.html", shorts=shorts)

if __name__ == "__main__":
    # ✅ Railway에서 포트를 환경변수로 받음
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
