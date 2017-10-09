# Care
Monitor web page change that you care


# Docker
It's difficult to set up environment, install all dependencies for this project correctly, so we are using Docker. Dockerfile is included so you just need to build your image and container:

`docker build -t <image name> .`
`docker run -td <image name>`

* -td keeps container running in background

Cron is not included in docker so in order to run the job periodically, you need to have an entry like below in your crontab:

`* * * * * docker exec <container_id> bash /app/run`

## Share directory
Although Dockerfile can copy whole project into /app directory in container, it's more convienent to be able to read/write to some directory on server so that we can save persistent data like log and snapshots. 
To share directory, instead of running

`docker run -td <image name>`

run

`docker run -td -v <absolute path of directory to be shared>:/<path to shared directory in container> <image name>`

e.g. `docker run -td -v /Users/david/Project/Care:/app_host_shared care`

Change your cron job to

`* * * * * docker exec <container_id> python /app_host_shared/src/app.py`

This way it will use project directory outside of docker container

## API
`python web.py`

API also runs in the container, so we need to expose it via
`docker run -td -v <absolute path of directory to be shared>:/<path to shared directory in container> -p 8088:8088 <image name>`


# Installing chrome on ec2
If not using docker...
sudo yum --nogpgcheck localinstall https://intoli.com/blog/installing-google-chrome-on-centos/google-chrome-stable-60.0.3112.113-1.x86_64.rpm
