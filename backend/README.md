## Our techstack
### Python/Flask with Nginx proxy and MySQL database that makes calls to sep ollama api

backend structor structure:
```
.
├── README.md
├── compose.yaml
├── db
│   └── password.txt
├── proxy
│   ├── Dockerfile
│   └── conf
└── service
    ├── Dockerfile
    ├── controller.py
    ├── database.py
    ├── db_unit_test.py
    ├── main.py
    └── requirements.txt

```

🛠️ Tech Stack Overview

A containerized full-stack app using:

    Python (Flask) – API backend

    MariaDB – MySQL-compatible database

    Nginx – Reverse proxy

    Docker Compose – Service orchestration

    Ollama API – External AI integration
