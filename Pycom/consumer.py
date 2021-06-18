import paho.mqtt.client as mqtt
import base64
import json
import pprint

from luand import decodePayload

server = "eu.thethings.network"
up_topic = '+/devices/+/up'
user = "app_02" #Application ID
password = "ttn-account-v2.myhqlQ4IICToIOuJUvDvVygc6kBKRFmHPlrTXQoKVPE" #Application Acess Key

def on_message(mqttc, obj, msg):
	print("Received!!")

    #load json from mqtt msg payload
	m = json.loads(str(msg.payload,'utf-8'))
	pprint.pprint(m)
	
    #decode raw payload
	message =base64.b64decode(m['payload_raw'])

	print(decodePayload(message))

mqttc = mqtt.Client()
mqttc.username_pw_set(user,password)
mqttc.on_message = on_message
mqttc.connect(server, 1883, 60)
mqttc.subscribe(up_topic, 0)


mqttc.loop_forever()
