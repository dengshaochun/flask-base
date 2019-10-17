FROM python:3.6.8-alpine

COPY pip.conf /root/.pip/pip.conf

WORKDIR /opt/flask-base

COPY manage.py requirements.txt .env /opt/flask-base/
COPY static /opt/flask-base/static
COPY templates /opt/flask-base/templates
COPY app /opt/flask-base/app

RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /opt/flask-base/docker-entrypoint.sh

EXPOSE 5201

ENTRYPOINT ["sh", "/opt/flask-base/docker-entrypoint.sh"]

CMD ["run", "-h", "0.0.0.0", "-p", "5000"]
