from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop
import RPi.GPIO as GPIO
import time

class MyClient(TornadoWebSocketClient):
     def opened(self):
        self.send("connected")

     def received_message(self, m):
        print(m)
        if len(m) == 175:
            self.close(reason='Bye bye')
        if str(m) == "The server says: feed! back at you":
            GPIO.setmode(GPIO.BCM)

            gp_out = 4
            GPIO.setup(gp_out, GPIO.OUT)
            servo = GPIO.PWM(gp_out, 50)

            servo.start(0.0)

            servo.ChangeDutyCycle(7.5)
            time.sleep(0.5)

            servo.ChangeDutyCycle(2.5)
            time.sleep(0.5)

            servo.ChangeDutyCycle(7.5)
            time.sleep(0.5)

            GPIO.cleanup()

     def closed(self, code, reason=None):
         ioloop.IOLoop.instance().stop()

ws = MyClient('wss://fathomless-brook-60632.herokuapp.com/ws', protocols=['http-only', 'chat'])
ws.connect()

ioloop.IOLoop.instance().start()
