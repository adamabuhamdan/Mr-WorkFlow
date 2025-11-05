#!/bin/bash

# Creating directories
mkdir -p app/api
mkdir -p app/services
mkdir -p app/utils


# Creating files
touch app/__init__.py
touch app/main.py
touch app/config.py
touch app/api/__init__.py
touch app/api/chat.py
touch app/services/__init__.py
touch app/services/vector_store.py
touch app/services/llm_service.py
touch app/utils/__init__.py
touch app/utils/text_splitter.py
touch requirements.txt
touch Dockerfile
touch .env.example
touch .env

echo "Directory and files created successfully!"