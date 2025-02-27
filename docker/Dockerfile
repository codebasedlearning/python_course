# (C) 2025 A.Voß, a.voss@fh-aachen.de, info@codebasedlearning.dev

FROM python:3.13.2

# Create user to prevent installation of dependencies at root level.
RUN useradd -m pythonista

WORKDIR /opt/project
ADD . /opt/project
USER pythonista

# Install dependencies from requirements.
RUN pip install --no-cache-dir --user -r requirements.txt
