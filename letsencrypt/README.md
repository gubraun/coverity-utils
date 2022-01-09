# Using Letsencrypt SSL certificated with Coverity Connect

## Intial setup

## Renewing certificates
If properly installed, Letsencrypt's certbot takes care of renewing the SSL certificates in time. For a standard Apache or Nginx install, certbot can even update the configs for the web server, but this doesn't work for Coverity Connect. So we have to do this manually.

#### Step 1: Convert the Letsencrypt cert and private key in a PKCS12 keystore format
```
openssl pkcs12 -export -in /etc/letsencrypt/live/coverity.ddns.net/cert.pem -inkey /etc/letsencrypt/live/coverity.ddns.net/privkey.pem -name tomcat -out cert_and_key.p12
```

#### Step 2: Import the new cert and private key into the Connect keystore
```
/coverity/cov-platform-2021.06/jre/bin/keytool -importkeystore -deststorepass changeit -destkeystore ./keystore.jks -srckeystore cert_and_key.p12 -srcstoretype PKCS12
```
When asked whether to overwrite 'tomcat', answer yes.
