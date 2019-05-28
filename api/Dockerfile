FROM python:3.6.8-jessie

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

# Set up cron
RUN apt-get update && apt-get -y install -qq cron

RUN chmod 0777 swagger_server/load_data.py

# Every 5 minutes
# RUN echo "*/5 * * * * . $HOME/.profile && cd /usr/src/app && ./load_data.sh >> /var/log/cron.log 2>&1" | crontab

# Weekly
RUN echo "* * */7 * * . $HOME/.profile && cd /usr/src/app && ./load_data.sh >> /var/log/cron.log 2>&1" | crontab

RUN touch /var/log/cron.log
RUN chmod 0666 /var/log/cron.log

EXPOSE 80

# Run data load script on startup
CMD cron && /bin/bash load_data.sh >> /var/log/cron.log 2>&1 && python3 -m swagger_server
