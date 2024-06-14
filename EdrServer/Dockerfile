
FROM python:3.10-slim-buster


RUN apt-get update && apt-get install -y curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY . /usr/src/app

RUN pip install --upgrade pip
RUN pip install -r /usr/src/app/requirements.txt
RUN chmod +x /usr/src/app/start.sh

CMD ["sh", "-c", "/usr/src/app/start.sh"]