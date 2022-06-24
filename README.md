# cp4d-monitors
Additional monitors for IBM Cloud Pak for Data, which can be deployed either using the IBM Cloud Pak Deployer, or using regular command line commands. The monitors adhere to the zen-watchdog interface and will be added to the Events and Alerts of Cloud Pak for Data. These monitors focus more on the functional usage of IBM Cloud Pak for Data and can be used to provide more insights into how the Cloud Pak for Data platform is used by its business users.

# IBM Cloud Pak for Data custom monitors

Custom monitors which can be integrated directly in IBM Cloud Pak for Data 4.0 Platform Management events. 

**List of available monitors**
- Hello World<br>
  A simple end to end implementation of an IBM Cloud Pak for Data monitor

- [Platform Global Connections](documentation/cp4d-platform-global-connections/cp4d-platform-global-connections.md)<br>
  A monitor which counts the number of available Global Connections. For each connection a connection test is performed

These monitors are designed be deployed with the Cloud Pak Deployer automated deployment process. When monitors are deployed, the Cloud Pak Deployer will perform the following tasks:
- Enable OpenShift monitoring
- Configure a MonitorService for the zen-watchdog
- Build the monitor image and push it into a container registry
- Create a ConfigMap which contains the specification of the monitor

The ConfigMap is consumed by the zen-watchdog which creates a cronjob. This cronjob will run the monitor using the defined schedule. 

![Overview Monitors](dapper_monitor_content.drawio.png?raw=true "Overview Monitors")





