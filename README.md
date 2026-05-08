# AguroSite Django Project

This repository contains a Django project that uses MySQL via XAMPP and stores user profile pictures in `media/`.

## Prerequisites

- Python 3.14 (must match the virtual environment Python version)
- XAMPP with MySQL/MariaDB running
- Node.js and npm (optional, only if you want to build Tailwind CSS)

## Setup on a new machine

1. Clone the repository:

```powershell
git clone <repo-url> agurosite
cd agurosite
```

2. Create and activate a Python virtual environment:

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

4. If you plan to build or modify Tailwind CSS, install npm dependencies:

```powershell
npm install
```

## Database configuration

1. Start XAMPP and make sure MySQL is running.
2. Create the database used by this project:

```powershell
C:\xampp\mysql\bin\mysql.exe -u root -e "CREATE DATABASE IF NOT EXISTS agurodj_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

3. If your MySQL root user has a password, update `agurosite/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'agurodj_db',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '<your_mysql_password>',
    }
}
```

## Run migrations

```powershell
python manage.py migrate
```

## Create a superuser (optional)

```powershell
python manage.py createsuperuser
```

## Run the Django development server

```powershell
python manage.py runserver
```

Open the app in your browser at:

- `http://127.0.0.1:8000/gender/list/`
- `http://127.0.0.1:8000/user/list/`

## Optional: Build Tailwind CSS

If you change the Tailwind source file, run:

```powershell
npm run tailwind
```

This will compile `crud/static/css/input.css` into `crud/static/css/output.css`.

## Important notes

- The project uses `PyMySQL` for the MySQL connection.
- `requirements.txt` includes the needed dependencies.
- If you use a different MySQL user/password, update `agurosite/settings.py` accordingly.
- The `media/` folder stores uploaded profile pictures.
