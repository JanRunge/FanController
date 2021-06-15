#!/bin/bash
#      ^^^^ - NOT /bin/sh, as this code uses arrays

pids=( )
export FLASK_APP=web

# define cleanup function
cleanup() {
  for pid in "${pids[@]}"; do
    kill -0 "$pid" && kill "$pid" # kill process only if it's still running
  done
}

# and set that function to run before we exit, or specifically when we get a SIGTERM
trap cleanup EXIT TERM

flask run --host=0.0.0.0 &  pids+=( "$!" )
python3 main.py $1 & pids+=( "$!" )

wait # sleep until all background processes have exited, or a trap fires
