from flask import Flask, Response, render_template
import threading
import datetime
import time
import config


from announcer import MessageAnnouncer

app = Flask(__name__)
count = 0
announcer = MessageAnnouncer()      # Instance of the Announcer


def format_sse(data: str, event=None) -> str:
    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/events', methods=['GET'])
def events():
    def event_stream():
        msg_queue = announcer.listen()
        while True:
            msg = msg_queue.get()
            yield msg

    return Response(event_stream(), mimetype='text/event-stream')


@app.route('/ping')
def ping():
    global count
    count += 1
    msg = format_sse(data=f'pong-{count}')
    announcer.announce(msg=msg)
    return {}, 200


def background_task():
    while True:
        time.sleep(2)
        now = datetime.datetime.now()
        msg = format_sse(data=f'{now:%Y%m%d%H%M%S}')
        announcer.announce(msg=msg)


def main():
    app.run(host=config.BIND_IP, port=config.LISTEN_PORT, debug=True)


if __name__ == '__main__':
    threading.Thread(target=background_task).start()
    main()
