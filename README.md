# 🚀 HACKATHON PROJECT 2025
Self help
The chat support app straight out of your wildest dystopian dreams.

What is it?
We decided to create the ultimate tech support app
that protects our employees by scrubbing our clients messages
and making sure that our employees are safe but this goes both ways!
if one of our I serv.. I meant employees decides that they want to blast out against our customer 
our AI filtering system will filter there messages so our customer will have the best customer service


in all seriousness we created and app that filters messages for rude and fowl language and then 
makes it into a more pleasant message while keeping the original meaning 
this can me done both ways and we mainly aimed to show off how AI could be used to translate tonality of messages.
and with some tinkering even adjust meaning say if we wanted to make a chat app that reverses each message to its opposite meaning.


## 🛠️ Our Tech Stack  
**Full Stack App with Flutter Frontend & Python Backend**

This is a full-stack application featuring a **Flutter frontend** and a **Python backend**, both containerized using Docker for streamlined development and deployment. The project also integrates with **Ollama APIs**, which support both self-hosted and external service configurations.

---

## 📂 Project Structure

```
project-root/
├── backend/
│   ├── app/                 # Python application code
│   ├── Dockerfile           # Backend Dockerfile
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── flutter_application/ # Flutter project root
│       ├── android/         # Android specific files & build logic
│       ├── ios/             # iOS specific files & build logic
│       ├── web/             # Web specific files (index.html, etc.)
│       ├── lib/             # Core Flutter application code (Dart)
│       │   ├── chat/        # Example: Chat feature module
│       │   ├── login/       # Example: Login feature module
│       │   ├── navigation/  # Example: Navigation logic
│       │   ├── settings/    # Example: Settings feature module
│       │   ├── theme/       # Example: Theme logic
│       │   └── main.dart    # Main application entry point
│       ├── pubspec.yaml     # Flutter project dependencies & metadata
│       ├── Dockerfile       # Frontend Dockerfile (optional, e.g., for web build)
│       └── README.md        # Flutter specific README (if present)
```

---

## ⚡ Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- [Flutter](https://flutter.dev/docs/get-started/install) installed (for local development)
- [NVIDIA GPU Support for Docker (GPU-accelerated containers)](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) (if self-hosting Ollama)

---

## 🐳 Running with Docker

### 1. Backend Only

```bash
cd backend
docker compose up --build
```

---

### 2. Flutter Frontend Only


```bash
flutter run -d <whatever connected device>
```

---

You will need to have both an ollama server of some sort and the back end to have this project working 
provided in backend is an automatic setup script

---

## 🔧 Building the Flutter App (Locally)

```bash
cd frontend/flutter_application
flutter pub get
flutter build web # Or flutter build <platform>
```

The build output will be in `build/web` for web builds.

---

## ⚙️ Configuration

Set environment variables such as:

- `OLLAMA_API_BASE_URL`
- Backend API URLs for Flutter

These help manage connections between frontend, backend, and model-serving services.

---

## 🔗 API & Proxy

Our project uses hard coded end points as this was a HACKATHON project in

- Update main.py llm manager cpu and gpu  

```dart
    llm_manager_gpu = LLmanager(model="mistral", url='http://192.168.8.137:11434/api/generate')
    llm_manager_cpu = LLmanager(model="gemma:2b", url='http://192.168.8.137:11435/api/generate')
```
these urls need to be updated to your endpoint or api end point
this has only been tested with self hosted instance so there is no api key functionality 

- Configure CORS in your Python backend if requests come from a different origin (like the Flutter web app).

---


