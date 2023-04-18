# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.238.1/containers/ubuntu/.devcontainer/base.Dockerfile

# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="jammy"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

#####################POSTCOMMANDS#############
# RUN apt-get update && apt-get -y upgrade
# RUN apt install python3-pip
# RUN pip install requirements.txt



# NOT WORKING
# RUN wget https://gmic.eu/files/linux/gmic_3.1.4_ubuntu22-04_jammy_amd64.deb
# RUN sudo dpkg -i gmic_3.1.4_ubuntu22-04_jammy_amd64.deb
# RUN sudo apt update --fix-missing
# RUN sudo apt-get install -f

# identify docker 
ENV DOCKER_CONTAINER Yes