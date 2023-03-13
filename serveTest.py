from modelServer import ModelServer

if __name__ == "__main__":
    ms = ModelServer('localhost', 'test_rpc_queue')
    ms.start()