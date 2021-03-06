nginx

certbot --nginx --domains $DOMAINS --email $REGISTER_EMAIL --redirect --agree-tos --no-eff-email  --noninteractive #--test-cert

nginx -s stop

sleep 2

/home/backup.sh
