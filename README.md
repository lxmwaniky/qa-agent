# QA Agent

A simple AI-powered Question Answering (QA) agent built with Google ADK and Gemini models. This project demonstrates how to create an interactive agent that answers user questions concisely and clearly.

## Features

- Built with Google ADK for easy agent development
- Uses Gemini 3 Flash Preview model for fast responses
- Configurable via environment variables

## Prerequisites

- Python 3.12 or higher
- Google Cloud account with Vertex AI enabled
- uv package manager (for dependency management)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lxmwaniky/qa-agent.git
   ``` 
   ```bash
   cd qa-agent
   ```

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

## Environment Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your Google Cloud details:
   - `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID
   - `GOOGLE_CLOUD_LOCATION`: Region for Vertex AI (e.g., `us-central1`)
   - `GOOGLE_GENAI_USE_VERTEXAI`: Set to `TRUE` to use Vertex AI

## Usage

Run the agent locally:
```bash
uv run adk web
```

## Deployment

Follow these steps to deploy the QA Agent to Google Cloud.

### 1. Login to gcloud CLI
```bash
gcloud auth login
```

### 2. Setup Application Default Credentials (needed by the Python SDK)
```bash
gcloud auth application-default login
```

### 3. Set your project context
```bash
gcloud config set project <project-name>
```

### 4. Deploy to Cloud
Point the deploy command specifically to the `src/` folder to avoid zipping up your local `.venv` (this avoids the 8MB error).
```bash
uv run adk deploy agent_engine \
  --project=<project-name> \
  --region=us-central1 \
  --display_name="QA Agent Local" \
  src/
```
