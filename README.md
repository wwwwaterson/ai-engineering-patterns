# AI Engineering Patterns 🧠 🛠️

A curated collection of architectural patterns, practical implementations, and experiments focusing on **Generative AI**, **RAG (Retrieval-Augmented Generation)**, and **Agentic Workflows**.

This repository serves as a reference for building robust, production-grade AI applications, bridging the gap between "notebook experiments" and maintainable software engineering.

## 🚀 Tech Stack & Tools
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green?style=flat)
![OpenAI](https://img.shields.io/badge/OpenAI-API-black?style=flat&logo=openai)
![Docker](https://img.shields.io/badge/Docker-Container-blue?style=flat&logo=docker)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?style=flat&logo=pytorch)

## 📂 Repository Structure

Here is an overview of the modules included in this repository. Each directory contains a self-contained implementation of a specific AI pattern.

### [`01-rag-basics/`](./01-rag-basics)
**Foundations of Retrieval-Augmented Generation.**
- Simple ingestion pipelines using Vector Databases (ChromaDB/FAISS).
- Basic semantic search implementation.
- Context injection into LLMs for grounded answers.

### [`02-advanced-rag-pdf/`](./02-advanced-rag-pdf)
**Handling complex unstructured data.**
- Advanced chunking strategies (Recursive vs. Semantic splitting).
- PDF parsing and metadata extraction.
- **Hybrid Search** (Keyword + Semantic) and Re-ranking mechanisms (Cross-Encoders) for higher accuracy.
- *Focus: Reducing hallucinations in document-heavy workflows.*

### [`03-agents-tools/`](./03-agents-tools)
**Autonomous Agents and Tool Use.**
- Implementation of the **ReAct** pattern (Reason + Act).
- Custom tools creation (Math, API calls, Search).
- Orchestrating multi-step workflows where the LLM decides the execution path.
- *Use case: Automating tasks that require external data access.*

### [`04-fine-tuning-llama/`](./04-fine-tuning-llama)
**Model customization and optimization.**
- Techniques for Parameter-Efficient Fine-Tuning (**PEFT**) and **QLoRA**.
- Fine-tuning Llama models on custom datasets for specific domain tasks.
- Model evaluation metrics.

---

## ⚙️ Engineering Practices

As a Senior Software Engineer, I prioritize code quality and maintainability even in AI experiments. This project adheres to:

- **Clean Architecture:** Separation of concerns between LLM interaction logic, data processing, and application interfaces.
- **Type Hinting:** Full usage of Python types to ensure code reliability and better developer experience.
- **Security:** Strict environment management using `.env` files (no hardcoded API keys).
- **Reproducibility:** Dependency management via `requirements.txt` or `poetry`.

## 🛠️ Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR-USERNAME/ai-engineering-patterns.git](https://github.com/YOUR-USERNAME/ai-engineering-patterns.git)
   cd ai-engineering-patterns
