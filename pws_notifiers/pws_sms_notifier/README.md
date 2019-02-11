PWS SMS Notifier
================

This component has the responsibility of consuming all messages coming from our queue service (RabbitMQ) through the notifications routing key (pws.notifications.*) and publish the corresponding SMS alert.

At the moment, we are using Twilio API for sending the messages.

The needed structure for this to work is a JSON object like the next one:

```json
{
  "receiver_phones": "123123,456456,789789",
  "message": "This is an alert message"
}
```

### Run locally

```bash
$ make run
```

### Testing

```bash
$ make run-unittests
```
