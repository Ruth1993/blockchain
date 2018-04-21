#!/bin/bash
for i in {1..20}
do
    term -e python3 client_test.py 127.0.0.1 8081 test$i
done
