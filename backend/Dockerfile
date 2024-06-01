# Dockerfile

# Pull base image(以哪個 Image 為基底進行改良)
FROM python:3.9 as base


# Set work directory(設定當前工作目錄)
WORKDIR /backend-code

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/backend-code"
#ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1


# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir pipenv
COPY /backend/requirements.txt requirements.txt
RUN pip install -r requirements.txt
# RUN pip install git+https://github.com/accent-starlette/starlette-core.git@master#egg=starlette-core
# RUN pip install git+https://github.com/accent-starlette/starlette-files.git@master#egg=starlette-files
# RUN pip uninstall typing --yes


RUN apt-get update && apt-get install netcat-openbsd psmisc  -y 

COPY . /backend-code
EXPOSE 8000


ENTRYPOINT ["sh", "./docker-backend-entry.sh"]


