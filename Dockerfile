FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
	python-pip \
	libmysqlclient-dev \
	wget \
	unzip \
	fonts-wqy-zenhei \
	cron \
	vim

# Set the Chrome repo.
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Install Chrome.
RUN apt-get update && apt-get -y install google-chrome-stable

# Download Chrome Driver
RUN wget https://chromedriver.storage.googleapis.com/2.32/chromedriver_linux64.zip

RUN unzip chromedriver_linux64.zip
RUN rm chromedriver_linux64.zip

# Move driver to system PATH
RUN mv chromedriver /usr/local/bin/chromedriver

# upgrade the pip package to the latest version
RUN pip install --upgrade pip


RUN mkdir /app
COPY . /app


# Add crontab file in the cron directory
COPY crontab /etc/cron.d/care-cron
# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/care-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log


RUN pip --no-cache-dir install -r /app/src/requirements.txt


# Run the command on container startup
# CMD cron && tail -f /var/log/cron.log

