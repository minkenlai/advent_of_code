#!/bin/bash

if [ "$1"=="" ]; then
  echo "Usage: $0 [day #]"
  exit 1
fi

pbpaste > aoc2022/puzzles/puzzle$1.txt