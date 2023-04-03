import argparse
import base64
import configparser
import json
import logging
import time
import os
import signal
import sys

import pika

from modelCreator import ModelCreator

class ModelServer:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        
        parser.add_argument('config')
        args = parser.parse_args()

        config = configparser.ConfigParser()
        config.read(args.config)

        log_level = getattr(logging, config['log']['logLevel'].upper(), None)
        if not isinstance(log_level, int):
            raise ValueError('Invalid log level: %s' % config['log']['logLevel'])
        
        logging.basicConfig(filename=config['log']['fileName'], encoding='utf-8', format='%(asctime)s %(levelname)s:%(message)s', level=log_level)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['mq']['host']))
        self.channel = self.connection.channel()
        self.rpcQName = config['mq']['rpcQueue']

        self.channel.queue_declare(queue=self.rpcQName)
        self.model_creator = ModelCreator()

    def start(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.rpcQName, on_message_callback=self._callback)
        logging.info('Model server is waiting for messages.')
        self.channel.start_consuming()

    def _callback(self, ch, method, properties, body):
        msg = json.loads(body)
        logging.info('Received request of size %s bytes, language: %s, id: %s.', sys.getsizeof(base64.b64decode(msg["audio"])), msg["lang"], properties.correlation_id)
        start = time.time()
        res = {}
        try:
            recognizer = self.model_creator.get_model({"lang": msg["lang"]})
            predText = recognizer.predict(base64.b64decode(msg["audio"]))
            res = {"success": True, "text": predText}
        except Exception as ex:
            message = ex.args
            logging.error('Failed to process request. id: %s, result: %s, time: %s, message: %s', properties.correlation_id, res, time.time() - start, message)
            res = {"success": False}
        
        ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         properties.correlation_id),
                     body=json.dumps(res))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        logging.info('Request processed. id: %s, result: %s, time: %s.', properties.correlation_id, res, time.time() - start)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.default_int_handler)
    try:
        ms = ModelServer()
        ms.start()
    except KeyboardInterrupt:
        logging.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)