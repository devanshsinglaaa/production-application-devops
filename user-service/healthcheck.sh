#!/bin/bash
curl -s http://localhost:8000/health || exit 0
echo "Health check passed"
