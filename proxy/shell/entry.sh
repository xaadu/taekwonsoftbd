if [ -f "/sslfiles/bak_default.conf" ]
then
    /home/restore.sh
else
    /home/get_cert.sh
fi

echo "== crond starting..."
crond
echo "== crond started =="

nginx -g "daemon off;"
