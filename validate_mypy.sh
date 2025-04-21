#!/usr/bin/env bash


if [ "$(which mypy > /dev/null; echo $?)" -eq "1" ]; then
  echo "please install mypy: 'pip install mypy'"
else
  # mypy src/p0_base/prg_general_config_and_state.py
  # mypy src/p1_pixels/img_0_pixels.py


  for FILE_PY in *.py  */*/*.py; do
    echo
    echo $FILE_PY
    mypy $FILE_PY  --check-untyped-defs
  done

fi

