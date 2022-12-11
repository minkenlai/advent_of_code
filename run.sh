#!/bin/bash
if [ "$1"=="" ]; then
  echo "Usage: $0 [day #]"
  exit 1
fi

venv/bin/python3 -i -m aoc2022.day$1 aoc2022/inputs/day$1.txt
