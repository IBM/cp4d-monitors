# set base image (host OS)
FROM registry.access.redhat.com/ubi8/python-38

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./scripts /cp4d-monitoring-scripts

WORKDIR /cp4d-monitoring-scripts

USER 1001
ENTRYPOINT [ "/cp4d-monitoring-scripts/run_scripts.sh" ]
