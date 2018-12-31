 Tech test for Telefonica.
 
 Test instructions inside intructions.pdf file.
  
 Mongo will be at host's port 27107, Flask will use port 5000
 
---
### How to run

```sh
docker-compose up -d # Start MongoDB, with volumes in /var/bot_api/db/data/
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
 