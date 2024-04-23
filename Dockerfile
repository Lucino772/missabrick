#syntax=docker/dockerfile:1
FROM python:3.8-slim
EXPOSE 8080

WORKDIR /opt/app
COPY . /opt/app/

# Install Dependencies
RUN cat <<EOT | tr -d '\r' | /bin/bash
pip3 install --upgrade pip
pip3 install --no-cache-dir gunicorn
pip3 install --no-cache-dir -r requirements.txt
EOT

RUN cat <<-"EOT" | tr -d '\r' > /opt/app/start.sh
flask db upgrade
# flask data load
flask user demo
gunicorn "app:create_app()" -b 0.0.0.0:8000 -w 4
EOT

# Install Dependencies
RUN cat <<EOT | tr -d '\r' | /bin/bash
pip3 install --upgrade pip
pip3 install --no-cache-dir gunicorn
pip3 install --no-cache-dir psycopg2-binary
pip3 install --no-cache-dir -r requirements.txt
EOT

CMD [ "/bin/bash", "/opt/app/start.sh" ]
