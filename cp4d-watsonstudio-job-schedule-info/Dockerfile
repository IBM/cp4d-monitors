# set base image (host OS)
FROM registry.access.redhat.com/ubi8/python-38

# install dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt \
    && latest_release=`curl https://api.github.com/repos/IBM/cpdctl/releases/latest` \
    && cpdctl_version=`echo $latest_release |python -c "import json; import sys; obj=json.load(sys.stdin); print (obj['tag_name'])"` \
    && wget -c https://github.com/IBM/cpdctl/releases/download/${cpdctl_version}/cpdctl_linux_amd64.tar.gz -O - | tar -xz \
    && mv cpdctl /opt/app-root/bin \
    && chmod +x /opt/app-root/bin/cpdctl
    
COPY ./scripts /cp4d-monitoring-scripts

WORKDIR /cp4d-monitoring-scripts

USER 1001
ENTRYPOINT [ "sh", "/cp4d-monitoring-scripts/run_scripts.sh" ]
