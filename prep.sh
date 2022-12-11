#!/bin/bash
if [ "x$1" = "x" ]; then
  echo "Usage: $0 [day #]"
  exit 1
fi

touch aoc2022/inputs/day$1.txt
touch aoc2022/inputs/day$1-example.txt
touch aoc2022/puzzles/puzzle$1.txt

echo "paste input? [y]/n"
read DO_IT
if [ "$DO_IT" = "n" ]; then
  exit
fi
pbpaste > aoc2022/inputs/day$1.txt

echo "paste example? [y]/n"
read DO_IT
if [ "$DO_IT" = "n" ]; then
  exit
fi
pbpaste > aoc2022/inputs/day$1-example.txt

echo "paste puzzle? [y]/n"
read DO_IT
if [ "$DO_IT" = "n" ]; then
  exit
fi
pbpaste > aoc2022/puzzles/puzzle$1.txt