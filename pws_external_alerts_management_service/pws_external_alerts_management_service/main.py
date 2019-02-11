from flask import Flask, request
import logging

from configurelogging import ConfigureLogging
from configmanager import ConfigManager


app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/alerts", methods=["POST"])
def alerts():
    logger.info(request.json)
    return "Success"


def connector_loop():
    logger.info("Starting PWS external alerts management service API")
    app.run(debug=True, host="0.0.0.0", port=5001)


if __name__ == "__main__":
    config = ConfigManager().configuration
    ConfigureLogging(**config["logger"])
    connector_loop()
