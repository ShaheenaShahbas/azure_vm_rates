# Use an official Python runtime as a parent image
FROM python:3.12.2-alpine
ADD vmsamp.py .

# Install any needed dependencies specified in requirements.txt
RUN pip install requests psycopg2-binary schedule

CMD ["python", "./vmsamp.py"]
