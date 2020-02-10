FROM python:3.7-slim


# Enable unbuffered logging
ENV PYTHONUNBUFFERED=1

COPY requirements.in .
RUN pip install -r requirements.in

WORKDIR /frontend

RUN mkdir frontend

# Add the application
COPY . frontend/

EXPOSE 8000

CMD ["--worker-class aiohttp.GunicornWebWorker" ]
ENTRYPOINT [ "gunicorn", "frontend.main:create_app" ]
