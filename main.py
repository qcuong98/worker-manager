from flask import Flask, request, jsonify, render_template
import asyncio
from threading import Thread
from worker_manager import WorkerManager

worker_manager = WorkerManager()
app = Flask(__name__)

@app.route("/", methods = ["GET"])
def demo():
    return render_template('home.html')

@app.route("/add-task", methods = ["POST"])
def add_task():
    content = request.get_json()
    worker_manager.add_task(content['task'], int(content['difficulty']))
    return "OK", 200

@app.route("/view-workers", methods = ["POST"])
def view_workers():
    info = worker_manager.get_worker_status()
    return jsonify(info), 200

@app.route("/shutdown-worker/<uuid:worker_id>", methods = ["DELETE"])
def shutdown_worker(worker_id):
    worker_manager.shutdown_worker(worker_id)
    return "OK", 200

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    t = Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()
    task = asyncio.run_coroutine_threadsafe(worker_manager.main(), loop)

    app.run(host = "0.0.0.0", port = 8000, debug=False) 
