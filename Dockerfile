FROM python:3.12-slim

# Set environment variables (optional)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and activate the virtual environment
WORKDIR /studypal

# Copy requirements.txt and install dependencies
COPY ./requirements.txt /studypal/

## Initiating a DB before web app is created
RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev

RUN pip install -r requirements.txt

# Copy project files
COPY . /studypal/

# Setting environment variables
#EXPOSE 8000


# Apply database migrations and run the server
#CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic && python manage.py runserver 0.0.0.0:8000"]

COPY ./start.sh /studypal/
RUN chmod u+x /studypal/start.sh

CMD ["/studypal/start.sh"]
# To build the image from these settings
#

# docker build --no-cache -t studypal:1.0 .

# To check a list of the images that have been built/are available on your machine
# docker images

# For port forwarding to make the app accessible publicly
# docker run -p 8000:[containerport] --name [new-name] [imageid/imagername]


#DEBUGGING

#For checking logs and debugging
# docker logs [containername]

#Getting terminal for a running container  
# docker exec -it [containerid] /bin/bash