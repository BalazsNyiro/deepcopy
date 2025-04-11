#!/usr/bin/env bash


if [ "$(which mypy > /dev/null; echo $?)" -eq "1" ]; then
  echo "please install mypy: 'pip install mypy'"
else
  # mypy src/0_base/prg_general_config_and_state.py
  # mypy src/1_utils/img_pixels.py

  for FILE_PY in */*/*.py; do

    if [[ "$FILE_PY" != *"_test.py" ]]; then

      echo "===== normal py file, mypy type validation: $FILE_PY ====="
      mypy $FILE_PY

    fi

  done
fi

