# base python image
FROM python:3.10

# set the working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code
COPY . /app

# expose the application port
EXPOSE 8000

# Default command to run the Django server
CMD ["python", "manage.py", "runserver", "-p", "0.0.0.0:8000"]
