# Base image with Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY *.py .

# Expose as a CLI
ENTRYPOINT ["python", "/app/main.py"]


# docker build -t bilayers-test .

# docker run --rm -v "C:\Project\slides\DB:/data" bilayers-test --inputfile "/data/TestRon.ome.zarr" --outputfolder "/data/output" --show_progress
