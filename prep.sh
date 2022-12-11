#!/bin/bash
if [ "$1"=="" ]; then
  echo "Usage: $0 [day #]"
  exit 1
fi

touch aoc2022/inputs/day$1.txt
touch aoc2022/inputs/day$1-example.txt
touch aoc2022/puzzles/puzzle$1.txt
