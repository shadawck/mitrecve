FROM python:3-alpine
LABEL name mitrecve
LABEL src "https://github.com/remiflavien1/mitrecve"
LABEL dockerfile fractalizers
WORKDIR .
RUN pip3 install mitrecve
ENTRYPOINT ["mitrecve"]
CMD ["-h"]
