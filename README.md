This is a model server servise of telegram voice recognition project. This service reads requests from message queue and uses ML models to do voice2text recognition.   

Installation
1) clone project
2) make install
3) create config file
4) make run

to run tests
1) create config_test file
2) make run_tests


Docker
for docker see https://github.com/ReshitkoM/msg_recognition-backend


example config:
```
[log]
fileName=logFile.log
logLevel=info
  
[mq]
host= localhost
rpcQueue= rpc_queue
```


example config_test:
```
[log]
fileName=logFileTest.log
logLevel=info
  
[mq]
host= localhost
rpcQueue= test_rpc_queue
```
