#!/bin/bash
set -e

# --- Start Ollama CPU and GPU Instances + Pull Models (Idempotent) ---

CPU_CONTAINER_NAME="cpuollama"
GPU_CONTAINER_NAME="ollama"
VOLUME_NAME="ollama" # Using a shared volume as in your original script
REQUIRED_MODELS=("mistral" "gemma:2b")

# Function to start a container if it doesn't exist or is stopped
start_container() {
  local container_name=$1
  shift
  local docker_run_args=("$@")

  if [ "$(docker ps -q -f name=^/${container_name}$)" ]; then
    echo "Container '${container_name}' is already running."
    return 0 # Indicate success/already running
  elif [ "$(docker ps -aq -f status=exited -f name=^/${container_name}$)" ]; then
    echo "Restarting existing stopped container '${container_name}'..."
    docker start ${container_name}
    # Check if restart was successful
    if [ $? -eq 0 ] && [ "$(docker ps -q -f name=^/${container_name}$)" ]; then
        echo "Container '${container_name}' restarted."
        return 0 # Indicate success
    else
        echo "Failed to restart container '${container_name}'. Removing and attempting to create..."
        docker rm ${container_name} &> /dev/null || true # Remove forcibly, ignore errors if already gone
        # Fall through to create new container
    fi
  fi

  echo "Starting new container '${container_name}'..."
  docker run -d --name ${container_name} "${docker_run_args[@]}"
  sleep 2 # Give container time to initialize
  if [ "$(docker ps -q -f name=^/${container_name}$)" ]; then
     echo "Container '${container_name}' started successfully."
     return 0 # Indicate success
  else
     echo "Error: Failed to start container '${container_name}'."
     docker logs ${container_name} # Show logs on failure
     return 1 # Indicate failure
  fi
}

# Start CPU Ollama instance on port 11435
echo "--- Setting up CPU Ollama (port 11435) ---"
start_container "$CPU_CONTAINER_NAME" \
  -v "${VOLUME_NAME}:/root/.ollama" \
  -p "11435:11434" \
  "ollama/ollama"
CPU_STARTED=$?

# Start GPU Ollama instance on port 11434
echo "--- Setting up GPU Ollama (port 11434) ---"
GPU_CONTAINER_STARTED=1 # Default to failure state
if docker info | grep -q 'Runtimes:.*nvidia'; then
    start_container "$GPU_CONTAINER_NAME" \
      --gpus=all \
      -v "${VOLUME_NAME}:/root/.ollama" \
      -p "11434:11434" \
      "ollama/ollama"
    GPU_CONTAINER_STARTED=$?
else
    echo "NVIDIA Docker runtime not detected. Skipping GPU container startup."
    # Decide if you want a CPU instance on 11434 as fallback, or just skip.
    # Skipping for now, as cpuollama already exists on 11435.
fi

# --- Pull Required Models into the main 'ollama' container ---
# Only proceed if the target container started successfully
if [ ${GPU_CONTAINER_STARTED} -eq 0 ]; then
    echo "--- Pulling required models into '${GPU_CONTAINER_NAME}' ---"
    for model in "${REQUIRED_MODELS[@]}"; do
        echo "Pulling model: ${model}..."
        docker exec -it ${GPU_CONTAINER_NAME} ollama pull ${model}
        if [ $? -ne 0 ]; then
            echo "Warning: Command to pull ${model} finished with a non-zero status."
        fi
         echo "Finished attempting to pull ${model}."
    done
    echo "--- Model pulling finished ---"
elif [ ${CPU_STARTED} -eq 0 ]; then
     echo "GPU container '${GPU_CONTAINER_NAME}' did not start. Cannot pull models into it."
     # Optionally, pull into the CPU container if that's desired as a fallback
     # echo "--- Pulling required models into '${CPU_CONTAINER_NAME}' as fallback ---"
     # for model in "${REQUIRED_MODELS[@]}"; do ... docker exec ${CPU_CONTAINER_NAME} ...; done
else
    echo "Neither Ollama container is confirmed running. Skipping model pull."
fi


echo "--- Ollama setup script finished ---"
