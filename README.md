# Sponsorship Influencer Coordination Platform (v2)

This platform allows sponsors and influencers to coordinate campaigns. The second version uses a Vue.js frontend with a Flask backend, along with Redis for task management via Celery.

## Features

- **Sponsor Campaign Management**: Sponsors can create and manage their campaigns.
- **Influencer Coordination**: Influencers can browse campaigns, accept, or negotiate offers.
- **Secure Login**: Utilizes Flask-Security-Too and bcrypt for authentication.
- **Task Queue**: Celery is used to handle asynchronous tasks.
- **Data Caching**: Flask-Caching with Redis for enhanced performance.
- **Data Visualization**: Visualizations using Matplotlib.
- **Cross-Origin Resource Sharing (CORS)**: Flask-CORS is enabled for API communication between the Vue.js frontend and the Flask backend.

## Tech Stack

- **Frontend**: Vue.js, HTML, Bootstrap
- **Backend**: Flask
- **Database**: Flask-SQLAlchemy (using SQLAlchemy ORM)
- **Task Management**: Celery with Redis
- **Authentication**: Flask-Security-Too, Flask-Bcrypt
- **Data Caching**: Redis, Flask-Caching
- **API**: Flask-RESTful for building the API

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Node.js and npm
- Redis server
- Virtual Environment (optional but recommended)

## Libraries Used

Install the following Python dependencies by running `pip install -r requirements.txt`:

- celery==5.4.0
- Flask==3.0.3
- Flask_Bcrypt==1.0.1
- Flask_Caching==2.3.0
- Flask_Cors==4.0.1
- Flask_RESTful==0.3.10
- Flask_Security_Too==5.5.0
- flask_sqlalchemy==3.1.1
- Jinja2==3.1.3
- matplotlib==3.8.3
- redis==5.0.8

## Installation and Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/sponsorship-platform-v2.git
    ```

2. Navigate to the project folder:

    ```bash
    cd sponsorship-platform-v2
    ```

3. **Backend Setup:**

    - Navigate to the backend directory:

        ```bash
        cd backend
        ```

    - (Optional) Create a virtual environment:

        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```

    - Install backend dependencies:

        ```bash
        pip install -r requirements.txt
        ```

4. **Frontend Setup:**

    - Navigate to the frontend directory:

        ```bash
        cd frontend
        ```

    - Install frontend dependencies:

        ```bash
        npm install
        ```

5. **Redis Setup:**

    Ensure Redis is installed and running:

    - On Windows:

        ```bash
        start cmd /k "redis-server"
        ```

    - On Linux or macOS:

        ```bash
        redis-server
        ```

6. **Environment Configuration:**

    The application configuration, including sensitive information such as `SECRET_KEY`, database URIs, and other security-related settings, is stored in a `config.py` file located in the `backend` directory.

    The `config.py` file contains the following structure:

    ```python
    class DevelopmentConfig(Config):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/sponsorship_platform.db'
        SECRET_KEY = "thisissecter"
        SECURITY_JOIN_USER_ROLES = True
        SECURITY_PASSWORD_SALT = "thisissaltt"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        WTF_CSRF_ENABLED = False
        SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
        CACHE_TYPE = "redis"
        CACHE_REDIS_HOST = "localhost"
        CACHE_REDIS_PORT = 6379
        CACHE_REDIS_DB = 0
    ```

## Running the Application

### Windows

To start all the services on Windows, you can use the `start.bat` file:

1. After setting up the environment and installing dependencies, double-click the `start.bat` file or run it from the command line:

    ```bash
    start.bat
    ```

This will:

- Start the Redis server.
- Start the Flask backend application.
- Start the Celery beat scheduler and worker.
- Start the Vue.js frontend application.

Once all services are up and running, open your browser and visit `http://localhost:8080` to access the platform.

### Linux / macOS

For Linux or macOS, follow these steps to manually start each service:

1. **Start Redis server**:

    ```bash
    redis-server
    ```

2. **Start the backend application**:

    Open a new terminal and run:

    ```bash
    cd backend
    python app.py
    ```

3. **Start Celery beat**:

    Open another terminal and run:

    ```bash
    cd backend
    celery -A app.celery beat --loglevel=info
    ```

4. **Start Celery worker**:

    In another terminal, run:

    ```bash
    cd backend
    celery -A app.celery worker --pool=solo --loglevel=info
    ```

5. **Start the frontend application**:

    Open a new terminal, navigate to the `frontend` folder, and run:

    ```bash
    cd frontend
    npm run serve
    ```

Once all services are running, open your browser and visit `http://localhost:8080` to view the platform.

## License

This project is licensed under the MIT License.
