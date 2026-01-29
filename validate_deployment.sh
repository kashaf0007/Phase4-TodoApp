#!/bin/bash

# Validation script to run Kagent health checks
echo "Running health checks for the Todo Chatbot deployment..."

echo "Checking the health of todo-namespace and verifying if the frontend can reach the backend..."
echo "kagent \"Check the health of todo-namespace and verify if the frontend can reach the backend.\""

# Additional validation steps
echo "Validating deployment status..."
kubectl get pods -n todo-namespace

echo "Validating services..."
kubectl get services -n todo-namespace

echo "Validating ingress..."
kubectl get ingress -n todo-namespace

echo "Validation completed!"