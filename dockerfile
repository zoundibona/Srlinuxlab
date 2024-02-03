FROM ubuntu
RUN mkdir Script
COPY Script/L3VRF_SCRIPT.py /Script
RUN  apt update
RUN  apt install -y python3
RUN ["/bin/echo", "TEST"] 
