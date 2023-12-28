FROM ubuntu
RUN mkdir Script
COPY Script/VRF_Creation.py /Script
RUN  apt update
RUN  apt install -y python3
RUN ["/bin/echo", "TEST"] 
