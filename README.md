# Public Warning Notification System
The components under this repository conform the Public Warning Notification System (PWNS) module for the STOP-IT project. 
General documentation of the module is available at https://stop-it-project.eu/results/public-warning-notification-system/

# Architecture
The approach followed is that of a Microservice based architecture, where several services communicate with each other within the PWNS system. Only one API access point is offered to external parties (as an API gateway), which is secured by an authentication service, which can use OAuth requests. All the API calls which are available for the PWNS have been documented and are available for testing purposes at https://stopit-pws.worlsensing.com/mb/swagger/.
