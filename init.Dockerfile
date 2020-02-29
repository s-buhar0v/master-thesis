FROM centos:centos8.1.1911

COPY ./initscripts /app

WORKDIR /app

RUN yum install epel-release -y
RUN yum install jq -y

CMD ./init.sh