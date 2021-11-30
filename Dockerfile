FROM node:16.13.0

ENV HOME /root

WORKDIR /root

COPY . .

RUN npm install

EXPOSE 8000

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && node index.js