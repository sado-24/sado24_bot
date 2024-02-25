FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=configurations.settings
ENV DEBUG 1
WORKDIR /code

COPY . /code/

# Install dependencies
# RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Create a directory for static files
RUN mkdir -p /mnt/static

# Collect static files
RUN python manage.py collectstatic --noinput --clear

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "configurations.wsgi:application"]
