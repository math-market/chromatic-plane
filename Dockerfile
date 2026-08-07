# Sandbox image for this problem's checker.
#
# Deliberately minimal: a solver can read this file in ten seconds and know
# exactly what will run. This checker needs exact rational arithmetic, so
# sympy is installed — pinned, so the image is reproducible.
#
# You build this image yourself from the repository you just cloned, so the
# checker inside it is the checker you read — nothing is downloaded from us.
# To confirm rather than trust:
#
#   docker run --rm --entrypoint cat checker /task/check.py | diff - check.py
#
# The base image is pinned by digest, not by tag: a tag like `python:3.12-slim`
# moves over time, so without this two people building the same commit could get
# different environments and a settled result might not reproduce.
FROM python:3.12-slim@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de
RUN pip install --no-cache-dir sympy==1.13.3
WORKDIR /task
COPY check.py /task/check.py
USER 65534:65534
ENTRYPOINT ["python3", "/task/check.py"]
