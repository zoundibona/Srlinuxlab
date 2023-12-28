FROM ubuntu
RUN mkdir testrepo
COPY testfile /testrepo
RUN  apt update
RUN  apt install -y python3
RUN ["/bin/echo", "TEST"] 
