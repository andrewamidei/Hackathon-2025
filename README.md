HACKATHON PROJECT 2025





OUR TECH STACK
# Full Stack App with Flutter Frontend & Python Backend

This is a full-stack application featuring a Flutter frontend and a Python backend, both containerized using Docker for streamlined development and deployment. The project also integrates with Ollama APIs, which support both self-hosted and external service configurations.

---

## 📂 Project Structure

```
project-root/
│
├── backend/
│   ├── app/                  # Python application code
│   ├── Dockerfile            # Backend Dockerfile
│   └── requirements.txt      # Python dependencies
│
├── frontend/
│   └── flutter_application/  # Flutter project
│       └── Dockerfile        # Frontend Dockerfile (optional)
│
└── docker-compose.yml        # Orchestrates both containers
```

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- [Flutter](https://flutter.dev/docs/get-started/install) installed (for local development)
- [NVIDIA GPU support for Docker (GPU-accelerated containers)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) (if self hosting)
---

## 🐳 Running with Docker

### 1. Backend Only

```bash
cd backend
docker build -t my-backend .

```

### 2. Flutter Frontend Only

This Dockerfile is mainly used for building the Flutter web output:

```bash
cd frontend/flutter_application
docker build -t flutter-web .
```

### 3. Using Docker Compose

If you have a `docker-compose.yml` in the root:

```bash
docker-compose up --build
```

---

## 🔧 Building the Flutter App (Locally)

```bash
cd frontend/flutter_application
flutter pub get
flutter build web
```

The build output will be in `build/web`.

---

## 📆 API & Proxy

If your backend serves an API, make sure to update the Flutter app to point to the correct host (e.g. `localhost`, `127.0.0.1`, or the Docker service name in compose).

---

## 📦 Running Tests

### Backend (Python)

```bash
cd backend/app
pytest
```

### Flutter

```bash
cd frontend/flutter_application
flutter test
```

---

## 📝 Notes

- Remember to configure CORS in your backend if needed.
- For serving the Flutter web build in production, use nginx or Firebase hosting.

---

## 📍 License

MIT License.

