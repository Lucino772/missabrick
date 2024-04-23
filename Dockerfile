#syntax=docker/dockerfile:1
FROM python:3.8-slim
EXPOSE 8080

# Install nginx
RUN apt-get update && apt-get install nginx -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /opt/app

# Install gunicorn
RUN pip3 install gunicorn

# Install requirements
COPY requirements.txt /opt/app/
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy Flask application
COPY . /opt/app/

# Load data
RUN flask db upgrade
RUN flask data load
RUN flask user demo

# Install Dependencies
RUN cat <<EOT | tr -d '\r' | /bin/bash
pip3 install --upgrade pip
pip3 install --no-cache-dir gunicorn
pip3 install --no-cache-dir psycopg2-binary
pip3 install --no-cache-dir -r requirements.txt
EOT

CMD [ "/opt/app/start.sh" ]