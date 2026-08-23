#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$response" = "200" ]; then
    echo "OK"
    exit 0
else
    exit 1
fi
