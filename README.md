# care
Monitor web page change that you care


# Docker
It's difficult to set up environment, install all dependencies for this project correctly, so we are using Docker. Dockerfile is included so you just need to build your image and container:

`docker build -t <image_name> .`
`docker run -td <container_name>`

-td keeps container running

Cron is not included in docker so in order to run the job periodically, you need to have an entry like below in your crontab:

`* * * * * docker exec <container_id> bash /app/run`





# Installing chrome on ec2
If not using docker...
sudo yum --nogpgcheck localinstall https://intoli.com/blog/installing-google-chrome-on-centos/google-chrome-stable-60.0.3112.113-1.x86_64.rpm
