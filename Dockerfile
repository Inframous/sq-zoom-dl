FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    apt-get install -y wget gnupg2 unzip python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable=111.0.5563.64-1 && \
    rm -rf /var/lib/apt/lists/*

# Download and install ChromeDriver that matches the installed version of Chrome
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $NF}' | sed 's/\..*//') && \
    wget -q "https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION)/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/

# Create a non-root user to run the app


# Set the working directory to the home folder of the app user
WORKDIR /app


# Install requirements
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt

# Copy the Python app to the container
COPY app.py .


# Run the Python app
CMD ["python3", "app.py"]
