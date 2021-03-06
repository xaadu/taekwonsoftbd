FROM nginx:alpine

COPY ./default_test.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

RUN mkdir /sslfiles

COPY ./shell/ /home/

CMD ["nginx", "-g", "daemon off;"]
