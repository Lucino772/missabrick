# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim-bullseye as backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update & Upgrade
RUN apt update && apt upgrade -y && apt clean -y

# Install Nginx
RUN --mount=type=bind,source=docker/scripts/install-nginx.sh,target=install-nginx.sh \
    bash ./install-nginx.sh

# Install python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install --upgrade pip \
    && python -m pip install gunicorn psycopg2-binary \
    && python -m pip install -r requirements.txt \
    && python -m pip install supervisor

# Create working directory
WORKDIR /usr/src/app

# Copy
COPY ./docker/rootfs /
COPY . .

# Expose the port that the application listens on.
EXPOSE 80

# Environment Variables for backend
ENV MISSABRICK_PROXY__X_FOR=1
ENV MISSABRICK_PROXY__X_PROTO=1
ENV MISSABRICK_PROXY__X_HOST=1

# Set ENTRYPOINT and CMD
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD [ "/usr/local/bin/supervisord" ]