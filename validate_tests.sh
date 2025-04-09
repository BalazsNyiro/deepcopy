#!/usr/bin/env bash

for FILE_TEST in */*/*_test.py; do

	echo "===== run test: $FILE_TEST ====="
	python3 $FILE_TEST
done
