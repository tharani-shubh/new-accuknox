## 1. Create and Activate a Virtual Environment

Create a virtual environment for the project and activate it:

```bash
python -m venv env
```

### 2. Activate the Virtual Environment
Activate the virtual environment by running the following commands:

For Windows:

cd env\Scripts

activate

For macOS/Linux:

source env/bin/activate

### 3. Install Required Packages
Change the directory to the project root where requirements.txt is located, and install the necessary packages:

pip install -r requirements.txt

### 4. Make migrations for the models

python manage.py makemigrations

### 5. Migrate the Models
Apply the database migrations to set up your database schema:

python manage.py migrate

### 6. Start the Development Server
Run the development server to start the project:

python manage.py runserver
