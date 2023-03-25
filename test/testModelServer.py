import base64
import json
import unittest
import uuid

import pika

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
    
    def tearDown(self):
        self.channel.queue_delete(queue='test_callback_queue')
        self.channel.close()
        self.connection.close()

    def __getAudioSample(self, path):
        f = open(path, 'rb')
        b = f.read()
        f.close()
        bb = base64.b64encode(b)
        s = bb.decode('utf-8')
        return s

    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def testPredict(self):
        request = {"audio": self.__getAudioSample('test/data/test.ogg'), "lang": "EN"}

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='test_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(request))
        
        self.connection.process_data_events(time_limit=None)
        self.assertEqual(json.loads(self.response)["text"], "hi this is a test message for my first was recognition telegram boat")

    def testLangs(self):
        request = {"audio": self.__getAudioSample('test/data/testRU.ogg'), "lang": "RU"}

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='test_rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(request))
        
        self.connection.process_data_events(time_limit=None)
        self.assertEqual(json.loads(self.response)["text"], "привет это тестовое сообщение для моего телеграмм бота на русском языке")

if __name__ == "__main__":
    unittest.main()