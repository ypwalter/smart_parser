#!/bin/bash

if [ ! -f test_smoke.sh ]; then
  echo "[FAIL] You should execute the tests in default selftest folder."
  exit 1
fi

cp ../simple_analyzer.py lib/
if [ ! -f lib/simple_analyzer.py ]; then
  echo "[FAIL] Failed to find the simple analyzer."
  exit 1
fi

py.test
