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

Follow these steps to deploy the QA Agent to Google Cloud Vertex AI Agent Engine.

### Setup Google Cloud Project

1. **Sign into Google Cloud**:
   - If you're an existing user: Sign in via [Google Cloud Console](https://console.cloud.google.com/)
   - If you're a new user: Sign up for the [Free Trial](https://cloud.google.com/free/docs/free-cloud-features)

2. **Create or select a Google Cloud project**:
   - Create a new project at [Create Project](https://console.cloud.google.com/projectcreate) or use an existing one.

3. **Get your Google Cloud Project ID**:
   - Find it on your GCP homepage (alphanumeric with hyphens, not the numeric project number).

4. **Enable required APIs**:
   - Enable [Vertex AI API](https://console.cloud.google.com/apis/library/aiplatform.googleapis.com)
   - Enable [Cloud Resource Manager API](https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview)

### Set Up Your Coding Environment

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Set your default project** (optional):
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

### Deploy the Agent

Deploy from your terminal using the ADK CLI:

```bash
PROJECT_ID=your-project-id
LOCATION_ID=us-central1

uv run adk deploy agent_engine \
  --project=$PROJECT_ID \
  --region=$LOCATION_ID \
  --display_name="QA Agent" \
  src/
```

This packages your code, builds it into a container, and deploys it to Agent Engine. The process can take several minutes.

Upon successful deployment, note the `RESOURCE_ID` from the output (e.g., `751619551677906944`).

### Using the Deployed Agent

To interact with your deployed agent, use the query URL:

```
https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):query
```

You need:
- `PROJECT_ID` (e.g., "my-project-id")
- `LOCATION_ID` (e.g., "us-central1")
- `RESOURCE_ID` (from deployment output)

## Testing the Deployed Agent

### View Deployed Agent in Cloud Console

Navigate to [Agent Engine UI](https://console.cloud.google.com/vertex-ai/agents/agent-engines) to view your deployed agents.

### Find Project Information

Use Cloud Console or gcloud to get `PROJECT_ID`, `LOCATION_ID`, and `RESOURCE_ID`.

From Cloud Console: Go to Agent Engine page, select "API URLs", and copy the Query URL.

From gcloud:
```bash
gcloud projects list
gcloud asset search-all-resources \
  --scope=projects/$(PROJECT_ID) \
  --asset-types='aiplatform.googleapis.com/ReasoningEngine' \
  --format="table(name,assetType,location,reasoning_engine_id)"
```

### Test Using REST Calls

#### Check Connection
```bash
curl -X GET \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines"
```

#### Send an Agent Request

1. Create a session:
```bash
curl \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):query \
  -d '{"class_method": "async_create_session", "input": {"user_id": "u_123"}}'
```

Extract the `session_id` from the response.

2. Send a query:
```bash
curl \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):query?alt=sse \
  -d '{
    "class_method": "async_stream_query",
    "input": {
      "user_id": "u_123",
      "session_id": "YOUR_SESSION_ID",
      "message": "How do you say '\''I am coding'\'' in Swahili?"
    }
  }'
```

### Test Using Python

```python
# Create remote session
remote_session = await remote_app.async_create_session(user_id="u_456")

# Send queries
async for event in remote_app.async_stream_query(
    user_id="u_456",
    session_id=remote_session["id"],
    message="What's the weather in New York?",
):
    print(event)
```

### Clean Up Deployments

To avoid charges, delete the deployed agent:

```python
remote_app.delete(force=True)
```

Or delete via [Agent Engine UI](https://console.cloud.google.com/vertex-ai/agents/agent-engines).
