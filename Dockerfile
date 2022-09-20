FROM python:3.10.5

ADD kitchen.py .
# dependencies
RUN pip install requests flask
#expose port
EXPOSE 80
#run app
CMD ["python","-u","kitchen.py" ]