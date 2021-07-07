from flask import Flask, Response, render_template
import queue
import threading
import datetime
import time


app = Flask(__name__)

count = 0

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                print(f'Send {msg!r} to {self.listeners[i]!r}')
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


announcer = MessageAnnouncer()


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')



@app.route('/ping')
def ping():
    global count
    count += 1
    msg = format_sse(data=f'pong-{count}')
    announcer.announce(msg=msg)
    return {}, 200


@app.route('/listen', methods=['GET'])
def listen():
    def stream():
        messages = announcer.listen()  # returns a queue.Queue
        while True:
            msg = messages.get()  # blocks until a new message arrives
            yield msg

    return Response(stream(), mimetype='text/event-stream')


def main():
    app.run(host='0.0.0.0', port=12344, debug=True)


def background_task():
    while True:
        time.sleep(2)
        now = datetime.datetime.now()
        msg = format_sse(data=f'{now:%Y%m%d%H%M%S}')
        announcer.announce(msg=msg)


if __name__ == '__main__':

    threading.Thread(target=background_task).start()
    main()


# @app.get('/events')
# async def get_events():
#     header = {'Content-Type': 'text/event-stream',
#                 'Cache-Control': 'no-cache'}


