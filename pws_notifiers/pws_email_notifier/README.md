PWS Email Notifier
==================

This component has the responsibility of consuming all messages coming from our queue service (RabbitMQ) through the notifications routing key (pws.notifications.*) and publish the corresponding email alert.

The needed structure for this to work is a JSON object like the next one:

```json
{
  "receiver_emails": "test@worldsensing.com,test_2@worldsensing.com",
  "message_html": "&lt;html&gt;&lt;body&gt;&lt;h1&gt;FastPark Notification&lt;/h1&gt;&lt;p&gt;Irregular behavior for sector: 1&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;",
  "title": "Irregular behavior for sector: 1"
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

