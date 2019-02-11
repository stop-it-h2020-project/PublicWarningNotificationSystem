#!/bin/sh

# Set up environment variables
. ENV/api.env

# Copy an edited swagger
cp swagger.yaml swagger.edited.yaml

sed -i "s@ENV_BACKEND_SWAGGER@$BACKEND_SWAGGER@g" swagger.edited.yaml