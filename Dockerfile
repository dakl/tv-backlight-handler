FROM dakl/arm32-python-alpine-qemu:3.7.1-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /code
COPY . /code

CMD ["gunicorn", "run:app"]