# Project sse-event-viewer
Demonstrate a simple Flask (main.py) and FastAPI (fast.py) application that implements a basic webpage showing all received events.
The app includes a dummy generator of periodic events - containing a date-time string.
A further endpoint /ping can be used to manually trigger a 'pong' event - using and http GET via curl or browser.

## Service Port (See config.py)
port = 12344 [Default]

## Endpoints
* / = Render index.html and associated javascript code which subscribes to the /events endpoint to receive Server Sent Event stream, writing those events to an HTML table on the web page.
* /events = API though which clients can connect and receive a stream of asynchronous (SSE) events.
* /ping = endpoint that will echo text data sent to it back to the web client (browser, curl, etc.).

### Build and Execute FastAPI Version
Prerequisites:
* Install python 3.9 or greater
* Install git                    [gitbash for Windows]

Then:

```
git clone https://github.com/nickausten/sse-event-viewer.git
cd sse-event-viewer
py -m venv venv
source venv/Scripts/activate     [Linux/bash]
venv\Scripts\activate.bat        [Windows]
pip install -r requirements.txt
py fast.py                       [FastAPI version]
py main.py                       [Flask version]
```
