#!/bin/bash

mkdir -p ./ca/{root-ca,sub-ca,server}/{private,certs,newcerts,crl,csr}/

tree

sleep 1

clear

chmod -v 700 ./ca/{root-ca,sub-ca,server}/private

sleep 1

clear

touch ./ca/{root-ca,sub-ca}/index

openssl rand -hex 16 > ca/root-ca/serial
openssl rand -hex 16 > ca/sub-ca/serial

tree

echo -e "\n\nDirectory Structure built\n\n"

sleep 1

clear

cd ca/

openssl genrsa -out root-ca/private/ca.key 4096

openssl genrsa -out sub-ca/private/sub-ca.key 4096

openssl genrsa -out server/private/server.key 2048

tree

echo -e "\n\nAll private keys created"

sleep 1

clear

cp /home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/customResources/ssl-conf/root-ca.conf ./root-ca/root-ca.conf
# root-ca.conf file command here paste at ./root-ca/root-ca.conf

cd root-ca/

openssl req -config root-ca.conf -key private/ca.key -new -x509 -days 8000 -sha256 -extensions v3_ca -out certs/ca.crt

sleep 1

openssl x509 -noout -in certs/ca.crt

echo -e "\n\nca.crt file created\n\n"

sleep 1

clear

cd ../sub-ca

cp /home/local/ZOHOCORP/sayad-pt5854/ZohoWorkspace/customResources/ssl-conf/sub-ca.conf ./sub-ca.conf
# ./sub-ca.conf command here

openssl req -config sub-ca.conf -new -key private/sub-ca.key -sha256 -out csr/sub-ca.csr

sleep 1

cd -

cd ./../

tree

openssl ca -config ./root-ca/root-ca.conf -extensions v3_intermediate_ca -days 3650 -notext -in ./sub-ca/csr/sub-ca.csr -out ./sub-ca/certs/sub-ca.crt

sleep 1

tree

sleep 1

clear

openssl x509 -noout -text -in ./sub-ca/certs/sub-ca.crt

echo -e "sub-ca.crt file created"

sleep 1

clear

cd ./server/

openssl req -key private/server.key -new -sha256 -out csr/server.csr

sleep 1

cd ./../

tree

openssl ca -config ./sub-ca/sub-ca.conf -extensions server_cert -days 36500 -notext -in ./server/csr/server.csr -out ./server/certs/server.crt

sleep 2

echo -e "\n\nserver.crt created\n\n"

sleep 3

clear


pwd

echo "AM HERE"

cat ./server/certs/server.crt ./sub-ca/certs/sub-ca.crt > ./server/certs/chained.crt

sleep 2

cd ..

tree

echo -e "\nCertificate Creation Completed\n"