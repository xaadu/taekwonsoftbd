text=$(certbot renew --post-hook "nginx -s reload")

/home/backup.sh

now="$(date +'%d/%m/%Y') $(date +"%r")"

curl -X POST -d "log=$now
$text" http://taekwonsoftbdlog.zayedabdullah.com/
