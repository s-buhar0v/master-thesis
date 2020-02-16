FROM centos:centos8.1.1911

COPY ./init /app

WORKDIR /app

RUN yum install epel-release -y
RUN yum install jq -y

CMD ./init.sh