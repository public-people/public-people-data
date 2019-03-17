#!/bin/sh

set -e

until curl $1; do
  >&2 echo "$1 is unavailable - sleeping"
  sleep 1
done

>&2 echo "$1 is up"
