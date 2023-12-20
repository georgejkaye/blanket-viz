#!/bin/sh

# Make sure cron can see environment variables
printenv >> /etc/environment

# Set up stdour and stderr for docker logs
mkfifo /tmp/stdout /tmp/stderr
chmod 0666 /tmp/stdout /tmp/stderr
tail -f /tmp/stdout &
tail -f /tmp/stderr >&2 &

cron -f