import pika
from time import sleep

EXCHANGE='hivemind'
QUEUE_TOPICS= {
        'test': 'nervecenter.test',
        'metrics': 'nervecenter.metrics',
        'metrics.storage': 'nervecenter.metrics'
        }

class Nervecenter(object):

    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self._channel = self._connection.channel()
        self.setup(self._channel)

    def setup(self, channel):
        # declare exchange
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)
        # declare queues
        for k,v in QUEUE_TOPICS.items():
            channel.queue_declare(queue=k)
            channel.queue_bind(exchange=EXCHANGE, queue=k, routing_key=v)

    def consume(self):
       self._channel.basic_consume(self.callback, queue='test', no_ack=True)
       self._channel.start_consuming()

    def callback(self, channel, method, properties, body):
        print('Received: {}'.format(body))
        sleep(1)

if(__name__=='__main__'):
    nervecenter = Nervecenter()
    nervecenter.consume()

