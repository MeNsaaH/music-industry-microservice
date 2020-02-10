FROM python:3.7-slim

# get packages
RUN apt-get -qq update \
    && apt-get install -y --no-install-recommends \
        git\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.in .
RUN pip install -r requirements.in

# Enable unbuffered logging
ENV PYTHONUNBUFFERED=1

WORKDIR /email

# Add the application
COPY . .

EXPOSE 8081
ENTRYPOINT [ "python", "email_server.py" ]
