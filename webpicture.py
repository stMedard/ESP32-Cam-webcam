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
    led.on()
    await asyncio.sleep(0.5)
    cc = camera.capture()
    
    camera.deinit()
    led.off()
    buf = b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'+cc

    yield from picoweb.start_response(resp, content_type="multipart/x-mixed-replace; boundary=frame")
    yield from resp.awrite(buf)
    gc.collect()


def run():
    app.run(host='0.0.0.0', port=80, debug=True)
