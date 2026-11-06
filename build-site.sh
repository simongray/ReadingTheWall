#!/bin/sh
# Build the web edition of the book into site/. See website/build.py.
exec python3 "$(dirname "$0")/website/build.py" "$@"
