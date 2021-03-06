echo "Restoring..."

mkdir -p /etc/letsencrypt/live/$DOMAIN
cp /sslfiles/fullchain.pem /etc/letsencrypt/live/$DOMAIN/fullchain.pem
cp /sslfiles/privkey.pem /etc/letsencrypt/live/$DOMAIN/privkey.pem

cp /sslfiles/options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
cp /sslfiles/ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem

cp /sslfiles/default.conf /etc/nginx/conf.d/default.conf

echo "Restored"
