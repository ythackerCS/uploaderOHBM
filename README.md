# Preprocessing Pipe Line Neurodot -Container 

## Introduction

> This container creates projects for users, verfies them and enables them on xnat and uploads data for their projects. This is a NONXNAT container and was used for a conference (OHBM 2022) 

##  Design: 
  * Used python 
  * full list of packages needed: (listed within the Dockerfile.base)
    * requests
    * pyxnat 
  * Uses docker base: python:3.7.9-buster
    
   
##  How to use:
  > All the scripts are located within the "workspace/" dir - any edits you will need to make for your specific use case will be with "upload.py". Once edits are done run ./build.sh to build your docker container. Specifics to edit within docker are the Dockerfile.base file for naming the container, pushing to git and libraries used. 

  #command to run the script 

  > docker run -ti -v  $PWD:/workspace -w /workspace registry.nrg.wustl.edu/docker/nrg-repo/yash/uploaderohbm python upload.py
  > structure of run command:
  > {docker run}    {-v volumemount:what its address will be on the inside} {-w sets workspace directory} {name of docker container} {python scriptname.py}

  * NOTE this is NOT a container designed for XNAT use, it was a conference specific container made for project creation for a workshop at OHBM 2022
  * If you want GPU access that will be different please look at the documentation on the website 

## NOTES:  
  * The scripts workspace were written with conferense and setting specificity in mind so please keep that in mind as you use this code 
  * It is recommended that you have some experience working with docker and specficially building containers 
  
## Future: 
  
