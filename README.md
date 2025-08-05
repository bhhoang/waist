# Waist
## Introduction

## Table of Contents

- [Waist](#waist)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [How to run this app](#how-to-run-this-app)
    - [Using Docker](#using-docker)
      - [Prerequisites](#prerequisites)
      - [Running the application](#running-the-application)
    - [Manual Installation and Execution](#manual-installation-and-execution)
      - [Prerequisites](#prerequisites-1)
      - [Backend Setup](#backend-setup)
      - [Frontend Setup](#frontend-setup)

- Author: [bhhoang](https://github.com/bhhoang)
- Waist stands for Weather App Internship Submission Task. 
- I made this for the submission as AI Engineer Internship for PMA Accelerator
- Since it to show skill, I am not using streamlit or gradio, instead a basic react.js
## How to run this app

### Using Docker

This project is set up to run with Docker and Docker Compose.

#### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)

#### Running the application

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd waist
    ```

2.  **Run the application:**

    *   **On Linux/macOS:**

        You can use the provided shell script to run the application. It will prompt you to choose between a local or remote PostgreSQL database.

        ```bash
        chmod +x docker-run.sh
        ./docker-run.sh
        ```

    *   **On Windows:**

        You can use the provided batch script.

        ```bash
        docker-run.bat
        ```

    *   **Manual Docker Compose:**

        If you prefer to run docker-compose manually, you can choose one of the following options:

        *   **With a local PostgreSQL database (recommended for development):**

            This will use the `docker-compose.override.yml` to set up a local PostgreSQL container.

            ```bash
            docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
            ```

        *   **With a remote PostgreSQL database:**

            Before running the command, you need to set the `DATABASE_URL` environment variable to your remote database URL.

            ```bash
            # On Linux/macOS
            export DATABASE_URL="postgres://user:pass@host:port/dbname"

            # On Windows (Command Prompt)
            set DATABASE_URL="postgres://user:pass@host:port/dbname"

            # On Windows (PowerShell)
            $env:DATABASE_URL="postgres://user:pass@host:port/dbname"
            ```

            Then run docker-compose:

            ```bash
            docker-compose -f docker-compose.yml up --build
            ```

3.  **Access the application:**

    Once the containers are up and running, you can default access the frontend at [http://localhost:3000](http://localhost:3000) and the backend API at [http://localhost:8000](http://localhost:8000).

### Manual Installation and Execution

If you prefer to run the backend and frontend manually without Docker, follow these steps.

#### Prerequisites

*   [Python 3.13](https://www.python.org/downloads/)
*   [Node 22.x](https://nodejs.org/en/download/)
*   A running PostgreSQL instance.

#### Backend Setup

1.  **Navigate to the project root directory.**

2.  **Create and activate a virtual environment:**

    ```bash
    # On Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # On Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the application:**

    Open the `settings.toml` file and configure the `[database]` section with your PostgreSQL connection details.

    ```toml
    [database]
    url = "postgresql+psycopg2://user:password@host:port/dbname"
    ```

5.  **Run the backend server:**

    ```bash
    python main.py
    ```

    The default backend API will be available at `http://localhost:8000`.

    ##### Running with uv
    As an alternative to `pip` and `venv`, you can use [uv](https://docs.astral.sh/uv/), a fast Python package installer.

    After installing `uv` (e.g., `pip install uv`), you can create a virtual environment, install dependencies, and run the server:
    ```bash
    # Create venv and install dependencies
    uv venv
    uv sync

    # Run the server
    uv run main.py
    ```

    ##### API Documentation
    The default swagger-ui documentation for backend is available at http://localhost:8000/docs


#### Frontend Setup

1.  **Navigate to the `frontend` directory:**

    ```bash
    cd frontend
    ```

2.  **Install the Node.js dependencies:**

    ```bash
    npm install
    ```

3.  **Create a `.env` file** in the `frontend` directory and add the following line, pointing to your running backend API:

    ```
    REACT_APP_API_URL=http://localhost:8000
    ```

4.  **Run the frontend development server:**

    ```bash
    npm start
    ```

    The frontend default will be available at `http://localhost:3000`.
