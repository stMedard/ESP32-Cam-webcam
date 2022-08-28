import camera
import picoweb
import machine
import uasyncio as asyncio
import esp
import ulogging as logging

esp.osdebug(True)

led = machine.Pin(4, machine.Pin.OUT)

app = picoweb.WebApp('app')

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('app')


@app.route('/')
def index(req, resp):

    # parse query string
    req.parse_qs()
    flash = req.form.get('flash', 'false')
    if flash == 'true':
        led.on()

    camera.init()

    # wait for sensor to start and focus before capturing image  
    led.on()
    await asyncio.sleep(0.5)
    buf = camera.capture()

    camera.deinit()
    led.off()

    yield from picoweb.start_response(resp, "image/jpeg")
    yield from resp.awrite(buf)

def run():
    app.run(host='0.0.0.0', port=80, debug=True)