# 2212204 — DevOps Project

**Name:** Zainab Zia 
**Registration Number:** 2212204  
**Live URL:** http://18.215.253.189:8000

---

## Architecture

```
[GitHub Push]
      |
      v
[GitHub Actions CI]
  - flake8 lint
  - pytest tests
      |
      v
[GitHub Actions CD]
  - SSH into EC2
  - Copy source files
  - docker compose up --build
      |
      v
[AWS EC2 t2.micro - Ubuntu]
      |
      |---- [FastAPI App - port 8000]
                  |
            [PostgreSQL 15 - port 5432]
                  |
            [Named Volume: postgres_data]
```

---

## Project Structure

```
2212204-devops-project/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI routes
│   ├── database.py            # SQLAlchemy setup
│   ├── models.py              # Student model
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py        # pytest fixtures
│       ├── test_health.py
│       └── test_students.py
├── Dockerfile
├── docker-compose.yml         # Local development
├── docker-compose.prod.yml    # EC2 production
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
├── .dockerignore
├── .github/
│   └── workflows/
│       ├── ci.yml             # Lint + test pipeline
│       └── cd.yml             # Deploy to EC2 pipeline
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check — returns status, db connection, and student reg no |
| POST | /students | Create a new student record |
| GET | /students | Get all student records |
| GET | /students/{reg_no} | Get a single student by registration number |

---

## Local Setup

### Prerequisites

- Python 3.11
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone https://github.com/zainab-zia571/2212204-devops-project.git
cd 2212204-devops-project
```

### 2. Create virtual environment

Windows:
```bash
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create .env file

```bash
cp .env.example .env
```

Open `.env` and set these values:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB=studentsdb
DATABASE_URL=postgresql://postgres:postgres123@db:5432/studentsdb
```

### 5. Start with Docker Compose

```bash
docker compose up --build
```

Wait until you see:
```
app-1  | INFO:     Application startup complete.
app-1  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Running Tests Locally

### Automated tests

```bash
pytest app/tests/ -v
```

### Linter

```bash
flake8 app/ --max-line-length=100 --exclude=app/tests/__init__.py
```

---

## Manual API Testing

### Health check

```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status": "ok", "db": "connected", "student": "2212204"}
```

### Create a student

Windows (single line):
```bash
curl -X POST http://localhost:8000/students -H "Content-Type: application/json" -d "{\"reg_no\":\"2212204\",\"name\":\"Your Name\",\"email\":\"you@email.com\",\"course\":\"DevOps\"}"
```


### Get all students

```bash
curl http://localhost:8000/students
```

### Get single student

```bash
curl http://localhost:8000/students/2212204
```

### Stop containers

```bash
docker compose down
```


## Live EC2 Testing

### Health check

```bash
curl http://18.215.253.189:8000/health
```

### Create student on EC2

Windows:
```bash
curl -X POST http://18.215.253.189:8000/students -H "Content-Type: application/json" -d "{\"reg_no\":\"2212204\",\"name\":\"Your Name\",\"email\":\"you@email.com\",\"course\":\"DevOps\"}"
```


### Get all students from EC2

```bash
curl http://18.215.253.189:8000/students
```

---



### GitHub Secrets required

| Secret | Description |
|--------|-------------|
| EC2_HOST | Public IP of EC2 instance |
| EC2_SSH_KEY | Full contents of the .pem private key file |

---

## EC2 Manual Deployment

If you need to deploy manually without the CD pipeline:

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@18.215.253.189

# Go to app folder
cd ~/app

# Start containers
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d --build

# Check running containers
docker ps

# View app logs
docker compose -f docker-compose.prod.yml logs app

# View database logs
docker compose -f docker-compose.prod.yml logs db
```