#!/bin/bash
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health)
if [ "$response" = "200" ]; then
    exit 0
else
    exit 1
fi
