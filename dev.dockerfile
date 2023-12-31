# Stage 1: Build environment
FROM python:3.8 AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt




# Stage 2: Production environment
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy your Django project code into the container
COPY . .

# Expose the port your Django app will run on (usually 8000)
EXPOSE 8000

# # # Make the entrypoint script executable
# # RUN chmod +x entrypoint.sh

# # # Set the entrypoint to your custom script
# # ENTRYPOINT ["entrypoint.sh"]

# RUN python manage.py makemigrations
# RUN python manage.py migrate

# # Start the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]






#########################################################




# FROM python:3.9-alpine
# ENV PYTHONUNBUFFERED 1
# COPY ./requirements.txt /requirements.txt
# # Install postgres client
# RUN apk add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#     gcc libc-dev linux-headers postgresql-dev
# RUN pip install -r /requirements.txt


# RUN apk del .tmp-build-deps

# RUN mkdir /app
# WORKDIR /app
# COPY ./app /app

# EXPOSE 8000

# # [Security] Limit the scope of user who run the docker image
# RUN adduser -D user

# USER user