cp Dockerfile.base Dockerfile && \
./command2label.py ./xnat/command.json >> Dockerfile && \
docker build --no-cache -t xnat/uploaderohbm:latest .
docker tag xnat/uploaderohbm:latest registry.nrg.wustl.edu/docker/nrg-repo/yash/uploaderohbm:latest
rm Dockerfile
