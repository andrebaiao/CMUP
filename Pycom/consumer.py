import paho.mqtt.client as mqtt
import base64
import json
import pprint

server = "eu.thethings.network"
up_topic = '+/devices/+/up'
user = "app_02" #Application ID
password = "ttn-account-v2.myhqlQ4IICToIOuJUvDvVygc6kBKRFmHPlrTXQoKVPE" #Application Acess Key

def on_message(mqttc, obj, msg):
	print("WIATING:")

    #load json from mqtt msg payload
	m = json.loads(str(msg.payload,'utf-8'))
	pprint.pprint(m)

    #decode raw payload
	message =base64.b64decode(m['payload_raw'])
	pprint.pprint(message)
    #interpret temperature
	payload_meta = int.from_bytes(message,byteorder='little')
	print("Temperature = {}".format(payload_meta))

	print("-----------")
	byted = payload_meta.to_bytes(2, 'little')
	print(byted)

	unbyted = int.from_bytes(byted, "little")
	print(unbyted)

	u_type = ( ((2**2)-1) << 14 ) & unbyted
	print(u_type >> 14)

	u_day = ( ((2**3)-1) << 11 ) & unbyted
	print(u_day >> 11)

	u_hour = ( ((2**5)-1) << 6 ) & unbyted
	print(u_hour >> 6)

	u_min = ( ((2**6)-1) << 0 ) & unbyted
	print(u_min >> 0)

mqttc = mqtt.Client()
mqttc.username_pw_set(user,password)
mqttc.on_message = on_message
mqttc.connect(server, 1883, 60)
mqttc.subscribe(up_topic, 0)


mqttc.loop_forever()
