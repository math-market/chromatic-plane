# Sandbox image for this problem's checker.
#
# Deliberately minimal: a solver can read this file in ten seconds and know
# exactly what will run. This checker needs exact rational arithmetic, so
# sympy is installed — pinned, so the image is reproducible.
FROM python:3.12-slim
RUN pip install --no-cache-dir sympy==1.13.3
WORKDIR /task
COPY check.py /task/check.py
USER 65534:65534
ENTRYPOINT ["python3", "/task/check.py"]
