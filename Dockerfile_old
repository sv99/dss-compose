# Use the standard Nginx image from Docker Hub
FROM nginx

ENV HOME=/app

# Source code file
WORKDIR ${HOME}
COPY ./src ${HOME}/src
COPY ./Pipfile ${HOME}/Pipfile
COPY ./Pipfile.lock ${HOME}/Pipfile.lock

# install python, uwsgi, and supervisord
RUN apt-get update && \
    apt-get install -y --no-install-recommends supervisor uwsgi python3 \
        python3-pip python3-dev build-essential procps

RUN pip3 install --upgrade setuptools && \
    pip3 install --no-cache pipenv && pipenv install --system --deploy

# Copy the configuration file from the current directory and paste 
# it inside the container to use it as Nginx's default config.
COPY ./deployment/nginx.conf /etc/nginx/nginx.conf

# setup NGINX config
RUN mkdir -p /spool/nginx /run/pid && \
    chmod -R 777 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chgrp -R 0 /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    chmod -R g+rwX /var/log/nginx /var/cache/nginx /etc/nginx /var/run /run /run/pid /spool/nginx && \
    rm /etc/nginx/conf.d/default.conf

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./deployment/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
RUN ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini

COPY ./deployment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN touch /var/log/supervisor/supervisord.log

EXPOSE 8080:8080
CMD ["supervisord"]