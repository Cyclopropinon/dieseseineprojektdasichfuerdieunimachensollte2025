#!/bin/bash

uv run services/tcp_server.py --ndp&
sts_pid=$!

uv run main.py

kill "$sts_pid" 2>/dev/null && echo "TCP Server (PID $sts_pid) terminated."

wait "$first_pid" 2>/dev/null

