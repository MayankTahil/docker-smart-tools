FROM osixia/ubuntu-light-baseimage
RUN apt-get update && \
	apt-get -y install python3-pip && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN mkdir -p /usr/clm && \
	sed -i "s/^exit 101$/exit 0/" /usr/sbin/policy-rc.d
COPY ./data/* /usr/clm/
WORKDIR /usr/clm
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 get-agent.py && \
	chmod +x install_agent.bin && \
	chmod +x monit.sh
CMD ./install_agent.bin && ./monit.sh