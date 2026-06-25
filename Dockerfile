# 1. Start with an official, lightweight Python environment
FROM python:3.11-slim

# 2. Set the directory inside the container where our code will live
WORKDIR /app

# 3. Copy our requirements file in first to install libraries
COPY requirements.txt /app/

# 4. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our project files (scripts, .env, etc.) into the container
COPY . /app/

# 6. For now, let's tell it to run your tracker backend when it starts
CMD ["python", "tracker.py"]