 Tech test for Telefonica.
 
 Test instructions inside intructions.pdf file.
  
 Mongo will be at host's port 27107, Flask will use port 5000
 
 Obs: The `/messages` endpoint isn't within a `Resource` class because I didn't make time to study how to read `GET` parameters from the URI.
  So the `GET /messages?conversationId` must be a function view, letting the `POST /messages` be the only method in a `MessageDetail` class 
  and the `GET /messages` be a single method in a `MessageList` class (which isn't pythonic at all) 
 
 ---
 ### Resolving dependencies
 
```sh
pip install -r requirements.txt
```

if you get problems with `marshmallow`, install it with

```sh
pip install -U marshmallow --pre
```
 
 
---
### How to run

```sh
docker-compose up -d # Start MongoDB, with volumes in /var/bot_api/db/data/
pip install -r requirements.txt
APP_CONFIG=prod flask run
```
---
### Testing


```sh
pytest tests/
```

 -  Test coverage


```sh
coverage run -m pytest tests/
coverage report -m
```
---
### TODO

 - Use a WSGI!
 - Docker build
 - Decorator to validate UUID
 - Fix Collection.Messages.timestamp microseconds
 - Index in Collection Bots.bot_uuid
 - Index in Collection Messages.message_uuid
 - Index in Collection Messages.conversation_uuid
 - Test payload of error messages
 