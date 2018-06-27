import pika
from time import sleep

EXCHANGE='hivemind'

class Hivemind(object):

    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self._channel = self._connection.channel()
        self.setup(self._channel)

    def setup(self, channel):
        # declare exchange
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)
        # declare queues
        channel.queue_declare(queue='test')
        channel.queue_bind(exchange=EXCHANGE, queue='test', routing_key='nervecenter.test')

    def consume(self):
       self._channel.basic_consume(self.callback, queue='test', no_ack=True)
       self._channel.start_consuming()

    def callback(self, channel, method, properties, body):
        print('Received: {}'.format(body))

if(__name__=='__main__'):
    hivemind = Hivemind()
    hivemind.consume()

