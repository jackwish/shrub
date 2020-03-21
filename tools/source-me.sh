#!/bin/sh


if [ "$(uname -s)" = "Darwin" ]; then
  export PYTHONPATH=${PYTHONPATH}:$(dirname $(dirname $(greadlink -f $0)))
else
  export PYTHONPATH=${PYTHONPATH}:$(dirname $(dirname $(readlink -f $0)))
fi

echo $PYTHONPATH
