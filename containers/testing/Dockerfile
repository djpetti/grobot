FROM ubuntu:16.04

ENV DISPLAY=:0

# Install dependencies with apt.
RUN apt-get update && apt-get install -y firefox wget curl python3-pip git \
    default-jre xvfb

# Install chrome.
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
# Disable chrome's sandboxing, because it breaks in Docker.
RUN CHROME_FILE=`which google-chrome` && \
    mv $CHROME_FILE "$CHROME_FILE"-noargs && \
    echo "#!/bin/bash \ngoogle-chrome-noargs --no-default-browser-check --no-sandbox --no-first-run \"\$@\"" \
    		 > $CHROME_FILE && \
		chmod +x $CHROME_FILE

# Install current version of node.
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get install -y nodejs

# Install node packages.
RUN /usr/bin/npm install -g bower polymer-cli redux web-component-tester

# Install everything in bower.json.
ADD bower.json .
RUN bower install --allow-root

# Install python dependencies.
RUN pip3 install pyserial tornado motor

# Configure bower_components symlink.
RUN mkdir /grobot && ln -s /bower_components /grobot/bower_components
