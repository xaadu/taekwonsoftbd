# TaekwonSoftBD 

A software for Event Managing in Bangladesh Taekwondo Federation

# See Live

Here's the live version: [https://taekwonsoftbd.com/](https://taekwonsoftbd.com/)


## Ready

This will be in .env file.

```env
# DATBASE
MYSQL_ROOT_PASSWORD=

MYSQL_DATABASE=

MYSQL_USER=
MYSQL_PASSWORD=

# APP
SECRET_KEY=
DEBUG=
ALLOWED_HOSTS=

# PROXY
DOMAINS=
REGISTER_EMAIL=


# GLOBAL
DOMAIN=
IPLOOKUP_TOKEN=

# RE-CAPTCHA
CLIENT_KEY=
OWNER_KEY=
```

Then this command is enough:
```bash
docker-compose -f docker-compose-prod.yaml up --build
```

Now the app is up and Running

## Set Starting ID for Registered Player
Postgres:
```sql
ALTER SEQUENCE host_registeredplayer_id_seq RESTART WITH 1000;
```

MySQL (Not Tested):
```sql
ALTER TABLE host_registeredplayer AUTO_INCREMENT = 1000;
```

# Licence

This is a custom web application and licenced only to Bangladesh Taekwondo Federation.
