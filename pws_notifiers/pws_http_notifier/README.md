PWS HTTP Notifier
================

This component has the responsibility of consuming all messages coming from our queue service 
(RabbitMQ) through the notifications routing key (pws.notifications.*) and publish the 
corresponding HTTP call alert.

The needed structure for this to work is a JSON object like the next one:

```json
{
  "url": "http://www.example.com",
  "message": "This is an alert message",
  "format": 10
}
```

### Run locally

```bash
$ make setup
$ make run
```

### Testing

```bash
$ make run-unittests
```