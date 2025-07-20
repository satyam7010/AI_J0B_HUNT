# Deployment Guide

This guide explains how to deploy the AI Job Hunt system in various environments.

## Local Development Deployment

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- Ollama (for local LLM)

### Setup and Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-job-hunt.git
   cd ai-job-hunt
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. Create a `.env` file (see Configuration Guide)

5. Run the application:
   ```bash
   # Run both backend and frontend
   python main.py
   
   # Or run individually
   python run_backend.bat  # For backend only
   python run_dashboard.py  # For frontend only
   ```

## Docker Deployment

### Prerequisites

- Docker
- Docker Compose

### Setup and Run

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the application:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:8501

### Docker Compose Configuration

Create a `docker-compose.yml` file:

```yaml
version: '3'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    environment:
      - DATABASE_URL=sqlite:///data/job_applications.db
      - LLM_PROVIDER=ollama
      - LLM_MODEL=gemma:3.4b
      - API_HOST=0.0.0.0
      - API_PORT=8000
    networks:
      - ai-job-hunt

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
    networks:
      - ai-job-hunt

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./ollama:/root/.ollama
    networks:
      - ai-job-hunt

networks:
  ai-job-hunt:
```

## Production Deployment

For production environments, consider the following adjustments:

### HTTPS Configuration

Enable HTTPS for production deployments:

1. Obtain SSL certificates (e.g., using Let's Encrypt)
2. Configure HTTPS in your reverse proxy (Nginx, Apache, etc.)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name yourdomainname.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomainname.com;

    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Frontend
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Cloud Deployment

For deploying to cloud platforms:

#### AWS Elastic Beanstalk

1. Create a `Procfile`:
   ```
   web: python main.py
   ```

2. Deploy using the EB CLI:
   ```bash
   eb init
   eb create
   eb deploy
   ```

#### Heroku

1. Create a `Procfile`:
   ```
   web: python main.py
   ```

2. Deploy using the Heroku CLI:
   ```bash
   heroku create
   git push heroku main
   ```

Note: For cloud deployments, consider using a cloud-based LLM provider like OpenAI instead of Ollama.

## Security Considerations

For production deployments:

1. Use environment variables for sensitive configuration (API keys, database credentials)
2. Implement proper authentication and authorization
3. Set up rate limiting to prevent abuse
4. Enable HTTPS for all traffic
5. Regularly update dependencies
6. Set up monitoring and logging
7. Use a web application firewall (WAF) for additional protection
