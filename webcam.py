import camera
import picoweb
import machine
import uasyncio as asyncio
import esp
import ulogging as logging
import gc

led = machine.Pin(4, machine.Pin.OUT)

esp.osdebug(True)

app = picoweb.WebApp('app')

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('app')


# Send camera pictures
def send_frame():
    buf = camera.capture()
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n'
           + buf + b'\r\n')
    del buf
    gc.collect()


@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/html")
 
    htmlFile = open('static/index.html', 'r')
 
    for line in htmlFile:
        yield from resp.awrite(line)
    gc.collect()


@app.route('/image')
def index_image(req, resp):

    camera.init()
    await asyncio.sleep(2)
    yield from picoweb.start_response(resp, content_type="multipart/x-mixed-replace; boundary=frame")
    while True:
        yield from resp.awrite(next(send_frame()))
        gc.collect()


def run():
    app.run(host='0.0.0.0', port=80, debug=True)




