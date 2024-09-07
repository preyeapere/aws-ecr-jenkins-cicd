FROM python:alpine
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
#RUN pip install --upgrade
CMD ["python","/main.py"]