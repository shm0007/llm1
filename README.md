
# 1. Application Overview

## 1.1 Application Description

This application is a **cybersecurity analysis system** that performs semantic search over vulnerability descriptions using the **CWE (Common Weakness Enumeration)** and **MITRE ATT&CK** datasets.

A user provides a vulnerability or attack description. The system:

1. Converts the input text into embeddings using selectable embedding models.
2. Performs semantic similarity search over the CWE and MITRE ATT&CK datasets stored in a vector database.
3. Retrieves relevant weaknesses and attack techniques.
4. Generates a contextualized security explanation using a large language model (LLM).

Supported LLM models include:

- Llama 3.1
- GPT-OSS

---

## 1.2 Major Components

| Component | Description |
|--------|--------|
| Frontend (Gradio) | Web user interface for entering vulnerability descriptions and viewing results |
| Backend (Flask API) | Handles embedding generation, vector search, and LLM inference |
| Weaviate | Vector database storing CWE and MITRE ATT&CK embeddings |
| Embedding Models | BERT, BGE, E5, LaBSE |
| Summmarizer LLM | Llama 3.1  |
| Docker Compose | Container orchestration for the system |

---

## 1.3 System Architecture

User → Frontend (Gradio) → Backend (Flask API) → Embedding Models  
Backend → Weaviate Vector Database → Backend → LLM → Frontend → User


# 2. Docker Materials

## 2.1 Docker Images

The system consists of three containers:

- llm1-backend
- llm1-frontend
- cr.weaviate.io/semitechnologies/weaviate:1.26.4 (official image)

Images can be loaded using:

`docker load -i <image-name>.tar`

---

## 2.2 Docker Image Details

### Weaviate (Vector Database)

Image:
cr.weaviate.io/semitechnologies/weaviate:1.26.4

Base Image:
Official Weaviate container image

Exposed Ports:
- 8080 — REST API

Persistent Storage:
weaviate_data:/var/lib/weaviate

---

### Backend (Flask API )

Image:
llm1-backend:latest

Base Image:
Python runtime with NVIDIA CUDA support

Exposed Port:
5002

GPU Requirement:
Requires NVIDIA GPU with Docker runtime enabled.

Environment Variable:
HF_TOKEN — HuggingFace access token used to download gated models

---

### Frontend (Gradio UI)

Image:
llm1-frontend:latest

Base Image:
Python runtime

Exposed Port:
7860

---

# 3. Hardware Requirements

## 3.1 GPU Requirements

| Requirement | Value |
|--------|--------|
| GPU Required | Yes |
| Minimum GPU Memory | 48 GB VRAM recommended |
| GPU Type | NVIDIA GPU with CUDA support |

---

## 3.2 CPU & RAM Requirements

### Backend

| Resource | Requirement |
|--------|--------|
| CPU | Minimum 8 cores |
| RAM | Minimum 32 GB |

The backend loads embedding models and LLM models into memory.

### Frontend

Minimal resources required.

### Weaviate

Lightweight vector database.

---

# 4. Storage Requirements

### Weaviate

| Item | Value |
|----|----|
| Size | ~5 GB |
| Purpose | Store embeddings for CWE and MITRE ATT&CK datasets |
| Container Path | /var/lib/weaviate |

### Backend (Model Cache)

| Item | Value |
|----|----|
| Size | ~20 GB |
| Purpose | Store downloaded HuggingFace models |
| Container Path | /root/.cache/huggingface |

Docker volume mount:

hf_cache:/root/.cache/huggingface

---

# 5. Configuration

## Environment Variables

| Variable | Description |
|--------|--------|
| HF_TOKEN | HuggingFace token required to download gated models |

The system uses Llama models which require HuggingFace access approval from Meta. 


---

## Network Ports

| Component | Port |
|--------|--------|
| Backend API | 5002 |
| Weaviate | 8080 |
| Frontend | 7860 |

---

# 6. External Dependencies

| Service | Purpose |
|--------|--------|
| HuggingFace Model Repository | Used to download embedding and LLM models |

The backend downloads models once and caches them locally.

---

# 7. Local Run Instructions

1. Navigate to project root
2. Create `.env` file with this variable:

HF_TOKEN=<your_huggingface_token>

3. Build containers

`docker-compose build`

4. Start services

`docker-compose up`

5. — Access UI

http://localhost:7860

6. — Verify Backend

`curl http://localhost:5002/health`

Expected:

`{{"status":"ok"}}`

7. — Verify Weaviate

`curl http://localhost:8080/v1/.well-known/ready`

Expected:

READY



---

# 8. Health Checks & Behavior

### Health Endpoints

| Service | Endpoint |
|------|------|
| Backend | http://localhost:5002/health |
| Frontend | http://localhost:7860 |
| Weaviate | http://localhost:8080/v1/.well-known/ready |

View container health with:

docker ps

---

### Startup Time

Typical startup time is about **30 seconds**.

The backend may take longer during the first run while models download.

---

### Expected Messages

When the backend server is run properly: this message can be found:

```
Serving Flask app 'backend_app'
backend-1   |  * Debug mode: on
backend-1   |  * Running on all addresses (0.0.0.0)
backend-1   |  * Running on http://127.0.0.1:5002
backend-1   |  * Running on http://172.18.0.3:5002
```

### Possible Errors

| Error | Cause |
|------|------|
| Connection refused: weaviate | Weaviate not ready |
| CUDA out of memory | GPU insufficient |
| Model download failed | HuggingFace authentication issue |

---

# 9. Security & Licensing

The system uses **Llama models from HuggingFace**, which are gated models.

Users must request access from Meta via HuggingFace before downloading or running these models.
More details on Gated Repo: https://huggingface.co/docs/hub/models-gated

---

# 10. Test Materials

### Sample Query 

"Observable Symptoms:

When monitoring memory usage on the affected system using the'show task memory detail' command, I notice that the memory allocated to the 'TED-INFRA-COOKIE' process increases over time. Specifically:

* The 'TED-INFRA-COOKIE' process's memory usage grows by approximately 288 bytes every few seconds.
* The process's memory allocation is not being released, resulting in a steady increase in memory usage.
* Continued receipt and processing of specific update packets causes the memory usage to continue increasing, eventually leading to exhaustion of available memory.

Open Technical Questions:

* What triggers the continuous increase in memory allocation for the 'TED-INFRA-COOKIE' process?
* Why is the memory allocated to the 'TED-INFRA-COOKIE' process not being released after it is no longer needed?
* How can we prevent or mitigate the impact of receiving and processing these specific update packets on the system's memory usage?"

Model: BGE


### Expected Output
![Gradio UI](./sample.png)

