dockertop
=========

A top-like docker container monitor written in python.

Installation
============

```bash
git clone git@github.com:bcicen/dockertop.git
cd dockertop/
sudo python setup.py install
```

Configuration Options
=============

The default configuration file is ~/.dockertoprc and is composed in yaml. This location can be overwritten with the -c switch.

d_url - the docker instance to connect to, either a socket or ip:port. Defaults to the local socket 
```
d_url: unix://var/run/docker.sock
```

TODO
=============

Right now dockertop only supports getting process resource metrics from the local machine as it reads directly from /proc
