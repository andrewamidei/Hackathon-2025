#!/bin/bash
set -e

docker run -d -v ollama:/root/.ollama -p 11435:11434 --name cpuollama ollama/ollama

