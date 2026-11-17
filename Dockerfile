FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install the package using its project metadata and copy only runtime code.
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir .

# Run the readiness check by default. Other ailab modules can be supplied
# after the image name, for example: ailab.model_size 7000000000 fp16.
ENTRYPOINT ["python", "-m"]
CMD ["ailab.check_env"]
