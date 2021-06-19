import paho.mqtt.client as mqtt
import base64
import json
import pprint
import datetime
import requests

from luand import decodePayload

server = "eu.thethings.network"
up_topic = '+/devices/+/up'
user = "app_02" #Application ID
password = "ttn-account-v2.myhqlQ4IICToIOuJUvDvVygc6kBKRFmHPlrTXQoKVPE" #Application Acess Key

def on_message():
	print("Received!!")

    #load json from mqtt msg payload
	m = json.loads(str(msg.payload,'utf-8'))
	pprint.pprint(m)
	
    #decode raw payload
	message = base64.b64decode(m['payload_raw'])

	msg = decodePayload(message)
	print(decodePayload(message))

	#msg = (1, 2, 10, 0, 3, 10)
	day = int(msg[1]) + 1
	hour = msg[2]
	minu = int(msg[3]) + int(msg[5])
	flag = int(msg[4])
	patient_id = 1

	if flag == 0:
		pload = {
			"patient_id": patient_id,
			"day": day,
			"hour": hour,
			"minu": minu,
			"take": True
		}
	else: 
		pload = {
			"patient_id": patient_id,
			"day": day,
			"hour": hour,
			"minu": minu,
			"take": False
		}

	r = requests.post('http://localhost:9000/takepill',data = pload)

	print(r.text)


mqttc = mqtt.Client()
mqttc.username_pw_set(user,password)
mqttc.on_message = on_message
mqttc.connect(server, 1883, 60)
mqttc.subscribe(up_topic, 0)


mqttc.loop_forever()
