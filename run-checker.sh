#!/usr/bin/env bash
# Run this problem's checker on your submission, in a sandbox.
#
#   ./run-checker.sh my_submission.json
#
# The container gets no network, a read-only filesystem, no capabilities and no
# ability to gain privileges; your file is mounted read-only. You are running
# code from this repository, so you should be able to satisfy yourself about
# what it does — check.py is short and the Dockerfile above it is six lines.
#
# Build first:  docker build -t checker .
set -euo pipefail
SUB="${1:?usage: run-checker.sh <submission-file> [image]}"
IMAGE="${2:-checker}"
exec docker run --rm \
  --network none \
  --read-only \
  --memory 512m --cpus 1 --pids-limit 64 \
  --security-opt no-new-privileges \
  --cap-drop ALL \
  -v "$(cd "$(dirname "$SUB")" && pwd)/$(basename "$SUB"):/data/submission:ro" \
  "$IMAGE" /data/submission
