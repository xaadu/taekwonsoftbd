echo "Backing Up..."

if [ -f "/sslfiles/default.conf" ]
then
    rm -r /sslfiles/*
fi

cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /sslfiles/fullchain.pem 
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /sslfiles/privkey.pem 

cp /etc/letsencrypt/options-ssl-nginx.conf /sslfiles/options-ssl-nginx.conf
cp /etc/letsencrypt/ssl-dhparams.pem /sslfiles/ssl-dhparams.pem

cp /etc/nginx/conf.d/default.conf /sslfiles/default.conf

echo "Backed Up"
