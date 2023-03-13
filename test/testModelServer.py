import unittest
import json
import pika, uuid
import modelServer

class TestModelServer(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='test_callback_queue', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.__on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None
    
    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def testPredict(self):
        f = open('test/data/test.ogg', 'rb')
        b = f.read()
        f.close()

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='test_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=b)
        
        self.connection.process_data_events(time_limit=None)
        self.assertEqual(json.loads(self.response)["text"], "hi this is a test message for my first was recognition telegram boat")

if __name__ == "__main__":
    unittest.main()