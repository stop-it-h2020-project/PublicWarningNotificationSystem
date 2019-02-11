alert = {
    "id": 123,
    "title": "Gas leak in Numancia 1",
    "type": 10,
    "severity": 10,
    "description": "Sensor detected high values of toxic gas in the viccinity"
}

response_plan_httppost_cap = {
    "response_plan_id": "Response Twitter for Marc DEMO",
    "message_status": 20,
    "alert_category": 110,
    "alert_severity": 40,
    "actions": [30],
    "action_parameters": ["false_mvila@worldsensing.com"],
    "action_format": [20],
    "action_description": ["Description for response"],
    "action_body": ["Body for repsonse"],
    "action_trigger": [10],
    "accessibility": 10,
    "area": "Sample area",
    "geolocation": "000000000140000000000000004010000000000000"
}

notification_cap = b'<alert xmlns="urn:oasis:names:tc:emergency:cap:1.2"><identifier>123456789</identifier><sender>_test@worldsensing.com</sender><sent>2019-01-30 12:58:33+01:00</sent><status>_Actual</status><msgType>_Alert</msgType><scope>_Public</scope><info><category>Gas leak in Numancia 1</category><event>Response Twitter for Marc DEMO</event><urgency>_Immediate</urgency><severity>_Severity</severity><certainty>_Likely</certainty><senderName>_Worldsensing Public Warning System</senderName><headline>Warning Gas leak in Numancia 1</headline><description>Body for repsonse</description><area>Sample area</area></info></alert>'
