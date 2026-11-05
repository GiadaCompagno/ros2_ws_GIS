#!/usr/bin/env bash
# Scarica i pacchetti di terzi alle versioni fissate in robot.repos e installa le dipendenze.
# Da usare su un clone nuovo del repo.
set -e
cd "$(dirname "$0")"
vcs import src < robot.repos
git -C src/rslidar_sdk submodule update --init --recursive
rosdep update
rosdep install --from-paths src --ignore-src -y --skip-keys="rko_slam"
