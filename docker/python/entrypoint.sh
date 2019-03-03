#!/bin/bash
set -e
cmd="$@"

if [ "$RUN_PARSER" != "" ];
then
    python parser.py
fi

if [ "$KEEP_ALIVE" != "" ];
then
    tail -f /dev/null
fi

exec $cmd
