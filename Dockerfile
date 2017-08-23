FROM fnndsc/ubuntu-python3

RUN mkdir -p /usr/app && sed -i "s/^exit 101$/exit 0/" /usr/sbin/policy-rc.d
COPY ./* /usr/app/
WORKDIR /usr/app
RUN pip3 install --no-cache-dir -r requirements.txt 
RUN python3 get-agent.py && chmod +x install_agent.bin
CMD ./install_agent.bin && tail -f /dev/null