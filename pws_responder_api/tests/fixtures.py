alert = {
    "title": "Gas leak in Numancia 1",
    "description": "Sensor detected high values of toxic gas in the viccinity"
}


response_plan_email = {
    "actions": [10],
    "action_parameters": ["email0@worldsensing.com"],
    "action_body": ["Gas leak in Numancia 1"],
    "action_format": [10]
}

response_plan_email_no_email = {
    "actions": [10],
    "action_format": [10],
    "action_body": ["Gas leak in Numancia 1"]
}

response_plan_sms = {
    "actions": [20],
    "action_parameters": ["555555555"],
    "action_format": [10],
    "action_body": ["Gas leak in Numancia 1"]
}

response_plan_sms_no_phone = {
    "actions": [20],
    "action_format": [10],
    "action_body": ["Gas leak in Numancia 1"]
}

response_plan_httppost = {
    "actions": [30],
    "action_parameters": ["http://stup-id.com:4000/alerts"],
    "action_format": [10],
    "action_body": ["Gas leak in Numancia 1"],
}

response_plan_httppost_no_url = {
    "actions": [30],
    "action_format": [10],
    "action_body": ["Gas leak in Numancia 1"]
}

response_plan_unkown_action = {
    "actions": [40],
    "action_parameters": ["http://stop-it.com:4000/alerts"],
    "action_format": [10],
    "action_body": ["Gas leak in Numancia 1"]
}
