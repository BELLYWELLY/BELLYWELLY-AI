FROM python:3.10
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1-mesa-glx
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./fastapi /code/app
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
