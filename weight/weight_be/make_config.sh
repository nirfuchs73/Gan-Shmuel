#! /bin/sh

cat > ./weights/config.py << END_OF_LINE
#! /usr/bin/env python3

DATABASE_HOST=$1
DATABASE_PORT=$2
DATABASE_DATABASE=$3
DATABASE_USER=$4
DATABASE_PASSWORD=$5
UPLOAD_FOLDER = '/app/in'

END_OF_LINE