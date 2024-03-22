FROM python:3.10.12-slim-buster
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the source code
COPY . /app/

# Run the application
CMD ["python", "manage.py", "runserver"]