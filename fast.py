from fastapi import FastAPI, Response, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse
# from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import datetime

import config
from announcer import MessageAnnouncer


app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
count = 0
announcer = MessageAnnouncer()      # Instance of the Announcer


@app.get("/")
async def home(request: Request):
    '''Return the main webpage template containing the event table'''
    return templates.TemplateResponse("index.html", {"request": request})


def my_generator(request):
    '''Generator to feed SSE event stream'''
    msg_queue = announcer.listen()
    while True:
        msg = msg_queue.get()
        yield msg


@app.get('/events')
async def events(request: Request):
    '''SSE Event stream endpoint'''
    event_generator = my_generator(request)
    return EventSourceResponse(event_generator)


@app.get('/ping')
async def ping():
    '''Use curl or browse this endpoint to create 'pong' event'''
    global count
    count += 1
    announcer.announce(msg=f'pong-{count}')
    return {}, 200


async def background_task():
    '''Background task creates event containing date and time every second'''
    while True:
        await asyncio.sleep(1.0)
        now = datetime.datetime.now()
        time_str = f'{now:%Y%m%d-%H%M-%S}'
        announcer.announce(msg=time_str)


@app.on_event('startup')
async def app_startup():
    '''Create and start our background_task()'''
    asyncio.create_task(background_task())


if __name__ == '__main__':
    uvicorn.run(app, host=config.BIND_IP, port=config.LISTEN_PORT,
                debug=config.DEBUG)
