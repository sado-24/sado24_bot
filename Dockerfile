FROM python:3.10-slim
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0  # Set DEBUG to 0 by default
# Set the working directory in the container
WORKDIR /code
# Copy the current directory contents into the container at /code
COPY . /code/
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Set up Django environment variables
ENV DJANGO_SETTINGS_MODULE=configurations.settings
# Collect static files and migrate database
# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "configurations.wsgi:application"]
