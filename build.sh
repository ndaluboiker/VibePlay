#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

# Apply any outstanding database changes (THIS IS THE KEY)
python manage.py migrate