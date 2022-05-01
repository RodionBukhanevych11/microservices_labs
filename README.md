```
pip3 install -e .
```

To run facade service
```
python3 microservices/facade/facade_service.py
```
To run message service
```
python3 microservices/message/messages_service.py
```
To run loggers services
```
python3 microservices/logging/logging_manager.py
```
or run loggers with all requests and then shutdown n of them
```
python3 microservices/app.py
```