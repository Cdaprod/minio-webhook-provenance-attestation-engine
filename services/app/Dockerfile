FROM python:3.12
# Copy your application code and the script
COPY . /app
# Install dependencies
RUN pip install -r /app/requirements.txt
# Make the script executable
WORKDIR /app
# Set the script as the entry point
CMD ["python", "main.py"]