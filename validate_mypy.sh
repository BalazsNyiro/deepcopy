#!/usr/bin/env bash


if [ "$(which mypy)" -eq "1" ]; then
  echo "please install mypy: 'pip install mypy'"
else
  mypy src/0_base/prg_general_config_and_state.py
  mypy src/1_utils/img_pixels.py
fi

