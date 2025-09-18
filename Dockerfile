FROM postgres:17.4

RUN apt-get install git
RUN cd /tmp
RUN git clone --branch v0.8.0 https://github.com/pgvector/pgvector.git
RUN cd pgvector
RUN make && make install
