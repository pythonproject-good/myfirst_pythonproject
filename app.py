from flask import Flask, render_template, jsonify, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# 전역 변수들
to_do_list = []
user_name = None

@app.route("/status")
def status():
    try:
        # 특정 작업이나 DB 연결 등을 확인하여 서버 상태 확인
        return jsonify({"status": "ok"})
    except Exception:
        return jsonify({"status": "error"}), 500

@app.route("/", methods=["GET", "POST"])
def index():
    global user_name
    if request.method == "POST":
        # 이름 입력 처리
        if "name" in request.form:
            user_name = request.form.get("name")
        # TODO 추가 처리
        if "task" in request.form:
            task = request.form.get("task")
            if task:
                to_do_list.append(task)
        return redirect(url_for("index"))
    return render_template("index.html", user_name=user_name, to_do_list=to_do_list)

@app.route("/time")
def get_time():
    """실시간 시간 데이터 제공"""
    now = datetime.now()
    return jsonify({
        "hours": now.hour,
        "minutes": now.minute,
        "seconds": now.second
    })

@app.route("/todos", methods=["GET", "POST"])
def manage_todos():
    """TODO 리스트 관리"""
    global to_do_list
    if request.method == "POST":
        task = request.json.get("task")
        if task:
            to_do_list.append(task)
    return jsonify(to_do_list)

@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_task(index):
    """TODO 삭제"""
    global to_do_list
    if 0 <= index < len(to_do_list):
        to_do_list.pop(index)
    return jsonify(to_do_list)

if __name__ == "__main__":
    app.run(debug=True)
