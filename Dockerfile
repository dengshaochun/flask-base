FROM python:3.6.4-slim-jessie

COPY pip.conf /root/.pip/pip.conf

WORKDIR /opt/flask-base

COPY . /opt/flask-base/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["bash", "/opt/flask-base/docker-entrypoint.sh"]
