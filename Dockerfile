FROM python:3.9

RUN set -x \
   && apt update \
   && apt upgrade -y \
   && apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
       packagekit-gtk3-module \
       python \
       pip \
       pulseaudio \
       pulseaudio-utils \
       curl \
   && pip install  \
       requests \
       selenium

ENV DEBIAN_FRONTEND noninteractive
ENV GECKODRIVER_VER v0.31.0
ENV FIREFOX_VER 97.0

# Add latest Firefox
RUN set -x \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

# Add geckodriver
RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/

# Install Poetry
RUN curl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

# Install Python Dependencies
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy Source Code
WORKDIR /app
COPY yttv.py .
ADD ./entrypoint.sh /entrypoint.sh

WORKDIR /app
ENTRYPOINT /entrypoint.sh
