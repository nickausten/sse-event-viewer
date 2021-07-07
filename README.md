# Project sse-event-viewer
Demonstrate a simple Flask application that implements a basic webpage showing all received events.
The Flask app includes a dummy generator of periodic events - containing a date-time string.

## Service Port
port = 12344

## Endpoints
* / = Render index.html and associated javascript code which subscribes to the /listen endpoint to receive Server Sent Event stream, writing those events to both console.log() and to an HTML table on the web page.
* /events = API though which clients can connect and receive a stream of asynchronous (SSE) events.
* /ping = endpoint that will echo text data sent to it back to the web client (browser, curl, etc.).
