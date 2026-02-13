#!/bin/bash

# Build and test Docker image locally before pushing to production

echo "Building Docker image..."
docker build -t cinemania:latest .

if [ $? -eq 0 ]; then
    echo "✓ Build successful!"
    echo ""
    echo "To test locally, run:"
    echo "docker run -p 8000:8000 -e SECRET_KEY='test-key' -e DEBUG='False' -e ALLOWED_HOSTS='localhost,127.0.0.1' cinemania:latest"
else
    echo "✗ Build failed!"
    exit 1
fi
