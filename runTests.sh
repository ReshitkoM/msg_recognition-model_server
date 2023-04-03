#!/bin/bash
python3 modelServer.py config_test &
P1=$!
python3 -m unittest discover -s ./test &
wait $!
echo $P1
kill -2 $P1