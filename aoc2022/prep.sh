#!/bin/bash
if [ "x$1" = "x" ]; then
  echo "Usage: $0 [day #]"
  exit 1
fi

touch inputs/day$1.txt
touch inputs/day$1-example.txt
touch puzzles/puzzle$1.txt

echo "paste input? [y]/n"
read DO_IT
if [ "$DO_IT" = "n" ]; then
  exit
fi
pbpaste > inputs/day$1.txt

echo "paste example? [y]/n"
read DO_IT
if [ "$DO_IT" = "n" ]; then
  exit
fi
pbpaste > inputs/day$1-example.txt

echo "paste puzzle? [y]/n"
read DO_IT
if [ "$DO_IT" = "n" ]; then
  exit
fi
pbpaste > puzzles/puzzle$1.txt