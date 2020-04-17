FROM python:3.7

ENV HOME=/app

# Source code file
WORKDIR ${HOME}
COPY ./src ${HOME}/src
COPY ./Pipfile ${HOME}/Pipfile
COPY ./Pipfile.lock ${HOME}/Pipfile.lock
COPY ./deployment/app ${HOME}

RUN pip3 install --upgrade setuptools && \
    pip3 install --no-cache pipenv && pipenv install --system --deploy

EXPOSE 5000
CMD ["./wait-for-elastic.sh" ]