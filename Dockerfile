    FROM python:3.8

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV TZ=America/New_York

RUN ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

COPY ./ /app
# Create the log file to be able to run tail

# CMD cron && tail -f /app/logs/cron.log

# RUN mkfifo --mode 0666 /app/logs/cron.log

# ENV DATABASE_PATH=/app/app.db

# EXPOSE 80

WORKDIR /app

# RUN apt-get update && apt-get -y install nano
# Copy docker-cron file to the cron.d directory
# COPY ./app/crontab.txt /etc/cron.d/docker-cron

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/docker-cron

# Apply cron job
# RUN crontab /etc/cron.d/docker-cron

# ENV PYTHONPATH=/usr/bin/python3

CMD ["bash"]

#docker run --link tradingplatform_timescaledb_1:database --net tradingplatform_default -v "$PWD":/app -it  arkfundstracker:latest