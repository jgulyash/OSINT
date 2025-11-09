#!/bin/bash

# Test script for OSINT Dashboard API
echo "========================================"
echo "Testing OSINT Dashboard API Endpoints"
echo "========================================"

API_URL="http://localhost:8081"

echo ""
echo "1. Testing Health Check..."
curl -s "$API_URL/health" | python3 -m json.tool

echo ""
echo "2. Testing Dashboard Stats..."
curl -s "$API_URL/stats" | python3 -m json.tool

echo ""
echo "3. Testing Investigations List..."
curl -s "$API_URL/investigations?limit=5" | python3 -m json.tool

echo ""
echo "4. Testing Graph Stats..."
curl -s "$API_URL/graph/stats" | python3 -m json.tool

echo ""
echo "5. Testing Graph Overview..."
curl -s "$API_URL/graph/overview" | python3 -m json.tool

echo ""
echo "6. Testing Entity Search..."
curl -s "$API_URL/graph/search?query=example&limit=10" | python3 -m json.tool

echo ""
echo "========================================"
echo "All tests completed!"
echo "========================================"
