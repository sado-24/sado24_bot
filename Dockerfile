FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1
# Set up Django environment variables
ENV DJANGO_SETTINGS_MODULE=configurations.settings
# Set the working directory in the container
WORKDIR /code
# Copy the current directory contents into the container at /code
COPY . /code/
# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# Install Gunicorn
RUN pip install gunicorn
RUN python3 manage.py createsuperuser

RUN mkdir -p /code/staticfiles
VOLUME /code/static

RUN python manage.py collectstatic --noinput --clear

# Expose port 8000
EXPOSE 8000
# Start the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "configurations.wsgi:application"]