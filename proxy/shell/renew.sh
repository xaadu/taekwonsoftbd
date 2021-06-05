text=$(certbot renew --post-hook "nginx -s reload")

now="$(date +'%d/%m/%Y') $(date +"%r")"

curl -X POST -d "log=$now
$text" http://taekwonsoftbdlog.zayedabdullah.com/
