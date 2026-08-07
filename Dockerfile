# Sandbox image for this problem's checker.
#
# Deliberately minimal: you can read this file in ten seconds and know exactly
# what will run. You build it yourself from the repository you just cloned, so
# the checker inside the image is the checker you read — nothing is downloaded
# from us. To confirm that rather than take it on trust:
#
#   docker run --rm --entrypoint cat checker /task/check.py | diff - check.py
#
# This checker needs exact rational arithmetic, so sympy is installed, pinned.
# The base image is pinned by digest, not by tag, so the whole environment is
# fixed by this commit. A tag like `python:3.12-slim` moves over time, which
# would mean two people building the same commit could get different images.
FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de
RUN pip install --no-cache-dir sympy==1.13.3
WORKDIR /task
COPY check.py /task/check.py
USER 65534:65534
ENTRYPOINT ["python3", "/task/check.py"]
