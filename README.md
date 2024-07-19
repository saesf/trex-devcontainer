A simple [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) for [trex traffic generator](https://github.com/cisco-system-traffic-generator/trex-core) with a python script to generate udp traffic in stateless mode.
#bind interfaces to vfio driver:
cd /opt/trex-core/scripts/
python3 /opt/trex-core/scripts/dpdk_nic_bind.py  --bind vfio-pci 01:00.0 01:00.1
#runnging trex:
```bash
cd /opt/trex-core/scripts/
./t-rex-64 -i --stl
```
```bash
python3 src/udp_stl.py
```