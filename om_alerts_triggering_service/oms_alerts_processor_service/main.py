# -*- coding: utf-8 -*-
import logging
from configurelogging import ConfigureLogging
from configmanager import ConfigManager
from processor import AlertsProcessor


logger = logging.getLogger(__name__)
config = ConfigManager().configuration

if __name__ == '__main__':
    ConfigureLogging(**config["logger"])
    alerts_processor = AlertsProcessor() 
    alerts_processor.run()
