import paho.mqtt.client as mqtt
import random
from time import sleep

client = mqtt.Client('unique_test')
client.username_pw_set('mqtt','mqtt')
client.connect('localhost')

while True:
    client.publish('nervecenter/test', random.randint(0,9999))
    print('Delivered message')
    sleep(random.randint(1,3))
