# Cloud File Vault

Cloud File Vault is a lightweight, containerized cloud storage application designed to provide a simple and efficient interface for file management. The system enables users to upload, download, view, and delete files through a web-based interface while ensuring data persistence and portability.

## System Architecture

The application follows a multi-container architecture, separating concerns between services for improved scalability and maintainability:

- **Frontend**: Served using Nginx, responsible for handling client requests and delivering the user interface.
- **Backend**: A Flask-based REST API that manages file operations and business logic.

## Core Features

- File upload, download, viewing, and deletion through a web interface  
- Persistent storage using Docker volumes to ensure data durability  
- Real-time storage usage monitoring and enforcement of storage limits  
- Lightweight and modular design for ease of deployment and scaling  

## Storage Management

All user files are stored in a persistent Docker volume, allowing data to remain intact across container restarts or redeployments. The system also tracks storage consumption and enforces predefined limits to ensure efficient resource usage.

## Deployment

Cloud File Vault is designed for seamless deployment using Docker. Prebuilt images hosted on Docker Hub allow the application to be deployed on any compatible system with minimal setup:

```bash
docker pull <your-image>
docker run <your-options> <your-image>
