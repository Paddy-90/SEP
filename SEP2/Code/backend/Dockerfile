# Use the official Python base image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Copy the backend code to the working directory
COPY . .

# Expose the port on which the backend will run
EXPOSE 5000

# Start the backend server
#CMD ["flask", "--app", "api", "run", "--debug"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app", "--log-level", "debug"]