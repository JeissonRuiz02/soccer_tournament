# Soccer Tournament Management Application

## Overview

This application is designed to manage a soccer tournament, allowing users to enter match results, view statistics, and maintain historical data records. It provides a user-friendly interface to manage teams, tournaments, and match details.

## Features

- Add, edit, and delete teams.
- Create, view, and delete tournaments.
- Enter match results and automatically update team statistics.
- View league tables with detailed team statistics.
- Export match results to JSON for backup and historical records.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Pip
- Virtualenv

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/JeissonRuiz02/soccer_tournament.git
   cd soccer_tournament

2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Create and activate a virtual environment:**
```bash
pip install -r requirements.txt


4. **Apply the database migrations:**

```bash
python manage.py makemigrations
python manage.py migrate

5. **(Optional) Load backup data from JSON files:**
```bash
python manage.py load_results

6. **Run the development server:**
```bash
python manage.py runserver


