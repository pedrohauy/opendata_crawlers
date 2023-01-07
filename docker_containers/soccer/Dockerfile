FROM python:3.7
RUN apt-get update && apt-get -y install cron vim

COPY  /crawler /app
WORKDIR /app
RUN touch /app/log
RUN pip3 install -r requirements.txt

RUN (crontab -l ; echo "* * * * * /usr/local/bin/python3 /app/soccer.py >> /app/log") | crontab

# run crond as main process of container
CMD ["cron", "-f"]