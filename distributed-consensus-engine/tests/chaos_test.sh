#!/bin/bash

echo "====================================="
echo "      CHAOS TEST STARTED"
echo "====================================="

echo ""
echo "Current Leader:"
curl http://localhost:5001/leader

echo ""
echo ""
echo "Stopping Leader Node (node5)..."

docker stop node5

sleep 5

echo ""
echo "Checking Cluster Health..."

curl http://localhost:5001/
echo ""

curl http://localhost:5002/
echo ""

curl http://localhost:5003/
echo ""

curl http://localhost:5004/
echo ""

echo ""
echo "Triggering New Election..."

curl http://localhost:5001/elect

echo ""
echo ""
echo "New Leader:"
curl http://localhost:5001/leader

echo ""
echo ""
echo "====================================="
echo "      CHAOS TEST COMPLETED"
echo "====================================="