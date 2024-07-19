# Using the latest epitech image
FROM ubuntu:22.04

RUN apt-get -y update  && apt-get -y install build-essential wget cmake git libnuma-dev python3-pip python3-pyelftools meson ninja-build iproute2 pciutils clangd && pip3 install lbr-trex-client
RUN cd /opt && git clone https://github.com/cisco-system-traffic-generator/trex-core.git && cd trex-core/linux_dpdk && ./b configure && ./b build
# Configure our workspace
WORKDIR /workspaces