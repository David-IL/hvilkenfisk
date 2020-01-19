# NOTES:
#    - (22.02.2019) We here use fastapi docker only and build tensorflow in (from scratch)
#    - References:
#       - Darkflow-yolo image that enables running yolo on CPU only, see https://github.com/davvdg/darkflow-docker
#       - fastapi docker, see https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Pick up some opencv dependencies and vim to enable editing of (text-based) files in container
RUN apt-get update && apt-get install -y \
    python3 \
	python-pip \
	cython \
	git \
	libglib2.0-0 \
	libsm6 \
	libxext6 \
	libxrender1 \
	libfontconfig1 \
	wget \
	vim

# Install other Python requirements by pip, including opencv-python
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy local repo and files to container
#VOLUME [ "/app" ]
COPY ./app /app
WORKDIR /app/


# Set AWS environment variables for login
ENV AWS_SHARED_CREDENTIALS_FILE=/app/aws_credentials
ENV AWS_CONFIG_FILE=/app/aws_config
ENV GUNICORN_CMD_ARGS="--timeout 120"