apt-get -y update
apt-get -y upgrade
apt-get install -y ffmpeg

celery -A file_process worker -l info