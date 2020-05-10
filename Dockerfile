FROM python:3.8.1

WORKDIR /tmp
RUN git clone https://github.com/masaar/limp

WORKDIR /tmp/limp
RUN git checkout v6.1.0-package
RUN python -m pip install .

WORKDIR /usr/src/app
COPY . .

RUN python -m limp install_deps

EXPOSE 8081
CMD [ "python", "-m", "limp", "launch" ]
