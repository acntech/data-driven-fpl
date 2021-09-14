# [Choice] Tensorflow version: 2.6.0, 2.5.1, 2.4.3
ARG VARIANT="2.6.0"

FROM tensorflow/tensorflow:${VARIANT}-jupyter

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends python3.7 sudo

RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.7 /usr/bin/python3


RUN useradd -rm -d /home/vscode -s /bin/bash -g root -G sudo -u 1001 vscode
USER vscode

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
