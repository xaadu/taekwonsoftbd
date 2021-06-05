echo "== Backing Up..."

if [ -f "/sslfiles/default.conf" ]
then
    rm -r /sslfiles/*
fi

if grep -q "# managed by Certbot" "/etc/nginx/conf.d/default.conf"
then
  cp /etc/nginx/conf.d/default.conf /sslfiles/bak_default.conf
  echo "== Backed Up =="
else
  echo "== Not Redirected =="
fi
