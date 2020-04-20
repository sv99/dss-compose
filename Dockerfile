FROM python:3.7

ENV HOME=/app

WORKDIR ${HOME}
COPY ./Pipfile ${HOME}/Pipfile
COPY ./Pipfile.lock ${HOME}/Pipfile.lock

RUN pip3 install --upgrade setuptools && \
    pip3 install --no-cache pipenv && pipenv install --system --deploy

RUN useradd -d /app -s /bin/bash uwsgi
RUN chown uwsgi.uwsgi /app
USER uwsgi
COPY ./src ${HOME}/src
COPY ./migrations ${HOME}/migrations
COPY ./deployment/app ${HOME}

EXPOSE 5000
CMD ["./wait-for-elastic.sh" ]