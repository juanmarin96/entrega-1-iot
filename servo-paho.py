import paho.mqtt.client as mqtt
import time

"""-- Funcion de atencion cuando llega un mensaje -- """
def on_message(mosq, obj, msg):
  global state
  command = msg.payload.decode("utf-8")
  print("Command from MQTT broker is [" + str(msg.topic) +
        " Rotation angle is: " + command + "]")


"""-- Cliente mqtt -- """
mqtt_server = "localhost"
client=mqtt.Client()

client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_start()
client.subscribe("servo/rotation",0)
while True:
  time.sleep(1)
client.loop_stop()
