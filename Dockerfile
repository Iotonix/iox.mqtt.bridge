FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV TZ=GM
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone  
RUN mkdir /config
ADD ./requirements.txt /config
RUN pip3 install -r /config/requirements.txt
WORKDIR /app
COPY . .
ENTRYPOINT ["python3"]
CMD ["mqtt_bridge.py"]
