FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install kafka-python 
RUN pip install pandas 


# Copy consumer script
COPY consumer2.py .

# Run consumer script
CMD ["python", "consumer2.py"]
