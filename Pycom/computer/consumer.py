import paho.mqtt.client as mqtt
import base64
import json
import pprint

server = "eu.thethings.network"
up_topic = '+/devices/+/up'
user = "" #Application ID
password = "" #Application Acess Key

def on_message(mqttc, obj, msg):

    #load json from mqtt msg payload
	m = json.loads(str(msg.payload,'utf-8'))
	pprint.pprint(m)

    #decode raw payload
	message =base64.b64decode(m['payload_raw'])
    
    #interpret temperature
	temp = int.from_bytes(message,byteorder='little')/100
	print("Temperature = {}".format(temp))

mqttc = mqtt.Client()
mqttc.username_pw_set(user,password)
mqttc.on_message = on_message
mqttc.connect(server, 1883, 60)
mqttc.subscribe(up_topic, 0)

mqttc.loop_forever()
