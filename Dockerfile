FROM python:3.10 as build

ARG port
USER root

WORKDIR usr/src/IPFRecom

ENV PORT=$port
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY certificate.crt /usr/src/IPFRecom/
COPY private.key /usr/src/IPFRecom/
COPY en_f.csv /usr/src/IPFRecom/


FROM build as temp
COPY ContentFiltering_Rules.py .
COPY app.py .
COPY wsgi.py .
RUN pyarmor obfuscate wsgi.py


FROM build as dist
COPY --from=temp usr/src/IPFRecom/dist/ usr/src/IPFRecom
WORKDIR usr/src/IPFRecom


EXPOSE $PORT

CMD gunicorn wsgi:server --bind 0.0.0.0:$PORT --preload

# EXPOSE 803
# EXPOSE 443
# # CMD echo ls;echo SECOND COMMAND
# # CMD ["gunicorn","-w", "10", "-b", "0.0.0.0:8000", "wsgi:server","--certfile","/usr/src/IPFRecom/certificate.crt","--keyfile","/usr/src/IPFRecom/private.key"]
# CMD ["gunicorn","-w", "10", "-b", "0.0.0.0:443", "wsgi:server"]

# # gunicorn -w 1 --certfile "usr/src/IPFRecom/certificate.crt" --keyfile "/usr/src/IPFRecom/private.key" -b 0.0.0.0:803 wsgi:server

# EXPOSE 443



#   "--certfile", "usr/src/IPFRecom/lh_cert.pem", "--keyfile", "usr/src/IPFRecom/lh_pkey.pem",
# --certfile=lh_cert.pem --keyfile=lh_pkey.pem


#  docker build  -t uqibcast/ipf:v5 .
#  docker images
#  docker run -it -d -p 8000:8000 image_name
