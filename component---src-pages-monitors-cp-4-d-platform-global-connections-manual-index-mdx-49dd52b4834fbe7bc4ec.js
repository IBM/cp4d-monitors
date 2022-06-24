"use strict";(self.webpackChunkcloud_pak_deployer_monitors=self.webpackChunkcloud_pak_deployer_monitors||[]).push([[5610],{924:function(e,n,o){o.r(n),o.d(n,{_frontmatter:function(){return c},default:function(){return s}});var t=o(3366),r=(o(7294),o(4983)),a=o(7160),l=["components"],c={},i={_frontmatter:c},p=a.Z;function s(e){var n=e.components,o=(0,t.Z)(e,l);return(0,r.kt)(p,Object.assign({},i,o,{components:n,mdxType:"MDXLayout"}),(0,r.kt)("p",null,"This page will go through all manual steps to deploy the Platform Global Connections monitor, and in addition to delete it. "),(0,r.kt)("p",null,"The following pre-requisites are assumed:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"IBM Cloud Pak for Data is successfully deployed"),(0,r.kt)("li",{parentName:"ul"},"(Optional) Prometheus is configured. Refer to ",(0,r.kt)("a",{parentName:"li",href:"/IBM/cp4d-monitors/prometheus/"},"setup OpenShift Prometheus and Cloud Pak for Data ServiceMonitor")," for instructions")),(0,r.kt)("p",null,"This manual deployment will be based on:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Source of the Monitor is located in a Git Repository"),(0,r.kt)("li",{parentName:"ul"},"The Image will be pushed to the internal OpenShift Image Registry ")),(0,r.kt)("h2",null,"Deploy Monitor Global Platform Connections"),(0,r.kt)("h3",null,"Create Source Repository authorization secret"),(0,r.kt)("p",null,"Create a secret to access the Git Source repository"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export GIT_SOURCE_TOKEN=<GIT_TOKEN>\nexport CP4D_PROJECT=<CP4D_PROJECT>\n\ncat << EOF | oc apply -f -\napiVersion: v1\nstringData:\n  password: ${GIT_SOURCE_TOKEN}\nkind: Secret\nmetadata:\n  name: global-platform-connections-repo-auth\n  namespace: ${CP4D_PROJECT}\ntype: kubernetes.io/basic-auth\nEOF\n")),(0,r.kt)("h3",null,"Build the Monitor Image and push to the registry"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\nexport OPENSHIFT_IMAGE_REGISTRY=image-registry.openshift-image-registry.svc:5000/${CP4D_PROJECT}\nexport GIT_SOURCE_TOKEN=<GIT_TOKEN>\n\noc new-build https://iamapikey:${GIT_SOURCE_TOKEN}@github.com/IBM/cp4d-monitors \\\n --context-dir cp4d-platform-global-connections  \\\n --name cp4d-platform-global-connections \\\n --source-secret global-platform-connections-repo-auth \\\n --to ${OPENSHIFT_IMAGE_REGISTRY}/cp4d-platform-global-connections:latest \\\n --to-docker=true \\\n --namespace ${CP4D_PROJECT}\n")),(0,r.kt)("p",null,"Wait for the build to complete successfully"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\noc wait -n ${CP4D_PROJECT} --for=condition=Complete build/cp4d-platform-global-connections-1  --timeout=300s\n")),(0,r.kt)("p",null,"or to monitor the build process:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\noc logs -n ${CP4D_PROJECT} build/cp4d-platform-global-connections-1 -f\n")),(0,r.kt)("p",null,"Ensure the build finishes with the message ",(0,r.kt)("inlineCode",{parentName:"p"},"Push successful")),(0,r.kt)("h3",null,"Create the Cloud Pak for Data zen-watchdog monitor configuration"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'export CP4D_PROJECT=<CP4D_PROJECT>\nexport OPENSHIFT_IMAGE_REGISTRY=image-registry.openshift-image-registry.svc:5000/${CP4D_PROJECT}\n\ncat << EOF | oc apply -f -\nkind: ConfigMap\napiVersion: v1\nmetadata:\n  name: zen-alert-cp4d-platform-global-connections-monitor-extension\n  namespace: ${CP4D_PROJECT}\n  labels:\n    app: zen-adv\n    icpdata_addon: \'true\'\n    icpdata_addon_version: 4.3.0\n    release: zen-adv\ndata:\n  extensions: |\n    [\n      {\n        "extension_point_id": "zen_alert_monitor",\n        "extension_name": "zen_alert_monitor_cp4d-platform-global-connections",\n        "display_name": "Global Platform Connections monitor",\n        "details": {\n          "name": "cp4d-platform-global-connections",\n          "image": "${OPENSHIFT_IMAGE_REGISTRY}/cp4d-platform-global-connections:latest",\n          "schedule": "*/15 * * * *",\n          "event_types": [\n            {\n              "name": "global_connections_count",\n              "simple_name": "Number of CP4D Platform connections",\n              "alert_type": "platform",\n              "short_description": "Number of CP4D Platform connections",\n              "long_description": "Number of CP4D Platform connections: <global_connections_count>",                \n              "resolution": "none",\n              "reason_code_prefix": "80"\n            },              \n            {\n              "name": "global_connection_valid",\n              "simple_name": "Test CP4D Platform connection",\n              "alert_type": "platform",\n              "short_description": "Test CP4D Platform connection",\n              "long_description": "Test result CP4D Platform connection: <global_connection_valid>",                \n              "resolution": "Validate the connection properties",\n              "reason_code_prefix": "80"\n            }          \n          ]\n        }\n      }\n    ]\nEOF\n')),(0,r.kt)("p",null,(0,r.kt)("strong",{parentName:"p"},"Note:")," Once the ConfigMap above is created, the zen-watcher pod will detect it. Please check the log of zen-watcher pod for details. For example:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'\nexport CP4D_PROJECT=<CP4D_PROJECT>\nexport ZEN_WATCHER_POD=$(oc get po -l component=zen-watcher -o custom-columns=CONTAINER:.metadata.name --no-headers)\noc logs ${ZEN_WATCHER_POD}\n\ntime="2022-01-05 08:30:42" level=info msg=CleanUpStaleExtensions event="upgrade extensions: removing stale extensions from zen-alert-cp4d-platform-global-connections-monitor-extension to the database"\ntime="2022-01-05 08:30:42" level=info msg=processExtensionHandler event="processing action: create for extension" extension_name=zen_alert_monitor_cp4d-platform-global-connections\ntime="2022-01-05 08:30:42" level=info msg=watchConfigMap event="config zen-alert-cp4d-platform-global-connections-monitor-extension added"\n')),(0,r.kt)("h3",null,"Wait for zen-watchdog to create cronjob"),(0,r.kt)("p",null,"Get the watchdog-alert-monitoring-cronjob cronjob details of Cloud Pak for Data"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\n\noc get cronjob watchdog-alert-monitoring-cronjob -n ${CP4D_PROJECT}\n\nNAME                                SCHEDULE       SUSPEND   ACTIVE   LAST SCHEDULE   AGE\nwatchdog-alert-monitoring-cronjob   */20 * * * *   False     0        3m46s           7d3h\n")),(0,r.kt)("p",null,"This cronjob must run in order for the Global Platform Connections cronjob to be created. Optionally the schedule can be changed to trigger its execution. The pod zen-watchdog can be monitored for any error messages:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"\nexport CP4D_PROJECT=<CP4D_PROJECT>\nexport ZEN_WATCHDOG_POD=$(oc get po -n ${CP4D_PROJECT} -l component=zen-watchdog -o custom-columns=CONTAINER:.metadata.name --no-headers)\n\noc logs -n ${CP4D_PROJECT} ${ZEN_WATCHDOG_POD} -f\n")),(0,r.kt)("p",null,"The new monitor cronjob is created:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\noc get cronjob -n ${CP4D_PROJECT}\n\nNAME                                       SCHEDULE       SUSPEND   ACTIVE   LAST SCHEDULE   AGE\ncp4d-platform-global-connections-cronjob   */15 * * * *    False     0        31s             7d3h\n")),(0,r.kt)("p",null,"Most monitors require access to the Cloud Pak for Data /user-home folder to cache information. To test whether this mount point is already present on the monitor use the following command:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'export CP4D_PROJECT=<CP4D_PROJECT>\nexport CP4D_CRONJOB=cp4d-platform-global-connections-cronjob\noc set volume -n ${CP4D_PROJECT} cronjobs/${CP4D_CRONJOB} | grep "mounted at /user-home" | wc -l\n')),(0,r.kt)("p",null,"If the result is ",(0,r.kt)("inlineCode",{parentName:"p"},"0"),", patch the cronjob using the following command:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'oc patch cronjob -n ${CP4D_PROJECT} ${CP4D_CRONJOB} \\\n--type=json \\\n--patch \'[{"op": "add","path": "/spec/jobTemplate/spec/template/spec/containers/0/volumeMounts/-","value": {"name": "user-home-mount","mountPath": "/user-home"}}]\'\n')),(0,r.kt)("p",null,"Based on the schedule the cronjob will be executed. This will create a pod, which can be monitored:"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\noc logs -n ${CP4D_PROJECT} <PODNAME>\n")),(0,r.kt)("h2",null,"Rebuilding the image"),(0,r.kt)("p",null,"When changes are applied to the monitor, restarting the Build Config will re-build and push the image to the image registry. No other changed are required. The next time the cronjob is executed, the new version of the monitor image will be used"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\nexport CP4D_CRONJOB=cp4d-platform-global-connections-cronjob\n\noc start-build -n ${CP4D_PROJECT} cp4d-platform-global-connections\n")),(0,r.kt)("p",null,"Monitor the build using (use -2, -3 etc, based on the created build by the previous command):"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\noc logs -n ${CP4D_PROJECT} build/cp4d-platform-global-connections-2 -f\n")),(0,r.kt)("p",null,"Patch the cronjob so it will Always pull the image to ensure it will fetch the latest version once triggered"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},'oc patch cronjob -n ${CP4D_PROJECT} ${CP4D_CRONJOB} \\\n  --type=json \\\n  --patch \'[{"op":"replace","path":"/spec/jobTemplate/spec/template/spec/containers/0/imagePullPolicy","value":"Always"}]\'\n')),(0,r.kt)("h2",null,"Remove the Monitor"),(0,r.kt)("p",null,"Use the following commands to delete the monitor"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\nexport CP4D_CRONJOB=cp4d-platform-global-connections-cronjob\noc delete bc -n ${CP4D_PROJECT} cp4d-platform-global-connections\noc delete cm zen-alert-cp4d-platform-global-connections-monitor-extension\noc delete secret global-platform-connections-repo-auth\noc delete cronjob ${CP4D_CRONJOB}\n")),(0,r.kt)("h2",null,"Reset Cloud Pak for Data metrics configuration and influxdb"),(0,r.kt)("p",null,"If, during development, the zen-watchdog is unable to process events because of an incorrect configuration or naming convention, using the following steps to reset the zen-watchdog and its influxdb"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"export CP4D_PROJECT=<CP4D_PROJECT>\noc project ${CP4D_PROJECT}\n\noc exec -it zen-metastoredb-0 /bin/bash\ncp -r /certs/ /tmp/\ncd /tmp/ && chmod -R 0700 certs/\ncd /cockroach \n./cockroach sql --certs-dir=/tmp/certs/ --host=zen-metastoredb-0.zen-metastoredb\nuse zen;\ndrop table policies;\ndrop table products;\ndrop table monitors;\ndrop table monitor_events;\ndrop table event_types;\nexit\n\noc delete cronjob watchdog-alert-monitoring-cronjob watchdog-alert-monitoring-purge-cronjob zen-watchdog-cronjob diagnostics-cronjob\noc delete pod -l component=zen-watchdog\n")),(0,r.kt)("p",null,"Wait for the cronjobs to be re-created"),(0,r.kt)("p",null,"Acquire the Password for influxdb"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"oc get secret dsx-influxdb-auth -o yaml\n")),(0,r.kt)("p",null,"Copy the base64 encoded “influxdb-password”"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"base64 -d <base64 encoded data>\n")),(0,r.kt)("p",null,"Delete the influxdb entries"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre"},"oc exec -it dsx-influxdb-0 bash\ninflux -ssl -unsafeSsl\nauth\n<enter>admin\n\nDelete the events\n\nuse WATCHDOG;\ndrop measurement events;\n")))}s.isMDXComponent=!0}}]);
//# sourceMappingURL=component---src-pages-monitors-cp-4-d-platform-global-connections-manual-index-mdx-49dd52b4834fbe7bc4ec.js.map