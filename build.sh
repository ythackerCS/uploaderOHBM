cp Dockerfile.base Dockerfile && \
docker build --no-cache -t xnat/uploaderohbm:latest .
docker tag xnat/uploaderohbm:latest registry.nrg.wustl.edu/docker/nrg-repo/yash/uploaderohbm:latest
rm Dockerfile
