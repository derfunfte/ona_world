# Docker Build Instructions

## Building the Docker Image

The Docker image includes all dependencies from `requirements.txt` and is ready to run the text-to-speech application.

### Option 1: Using Docker directly

```bash
# Build the image
docker build -t meine-stimme-app .

# Run the container
docker run -p 7860:7860 -v $(pwd)/output:/app/output meine-stimme-app
```

### Option 2: Using Docker Compose (Recommended)

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

## What's Included

- **Base Image**: `aladdin1234/xtts-webui:0.2`
- **Dependencies**: All packages from `requirements.txt` are installed
- **Application**: Text-to-speech application (`meine_stimme_app.py`)
- **Port**: Application runs on port 7860
- **Output**: Audio files are saved to `./output` directory

## Files Created

- `Dockerfile` - Updated with proper requirements.txt integration
- `docker-compose.yml` - For easy container management
- `.dockerignore` - Excludes unnecessary files from build context

## Requirements.txt Dependencies

The following packages are installed in the Docker image:
- gradio==4.13.0
- torch==2.1.1
- torchaudio==2.1.1
- faster_whisper==0.10.0
- tts>=0.22.0
- And many more TTS-related dependencies...

## Usage

Once the container is running, access the application at:
- Local: http://localhost:7860
- In Gitpod: Use the preview URL provided by the environment