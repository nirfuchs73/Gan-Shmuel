#! /bin/sh

cat > ./weights/config.py << END_OF_LINE
#! /usr/bin/env python3

from secrets import token_urlsafe

DATABASE_HOST = $1
DATABASE_PORT = $2
DATABASE_DATABASE = $3
DATABASE_USER = $4
DATABASE_PASSWORD = $5
SECRET_KEY = token_urlsafe(35)

END_OF_LINE