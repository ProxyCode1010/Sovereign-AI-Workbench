#!/bin/bash
set -e
echo "Pulling models into ollama container (run BEFORE isolating network, or temporarily attach ollama to a bridge with internet)..."
docker exec sw_ollama ollama pull qwen2.5:1.5b-instruct
docker exec sw_ollama ollama pull qwen2.5-coder:1.5b
docker exec sw_ollama ollama pull moondream:1.8b
docker exec sw_ollama ollama pull nomic-embed-text
echo "Done. Now restart compose with internal networks enforced."