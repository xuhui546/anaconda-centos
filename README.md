# anaconda-centos

A Dockerfile that produces a Docker Image for anaconda3 on centos7.

## anaconda version

The `master` branch currently hosts centos7.2.1511 and  anaconda3.4.1.1.

Different versions of anaconda are located at the github repo [branches](https://github.com/xuhui546/anaconda-centos/branches).

## Usage

### Build the image

To create the image `xuhui546/anaconda-centos`, execute the following command on the `anaconda-centos` folder:

```
$ docker build -t xuhui546/anaconda-centos .
```

### Run the image

To run the image and bind to host port 8888:

```
$ docker run -d -p 8888:8888 xuhui546/anaconda-centos /bin/bash -c \
"python /root/cfg_notebook.py -p 8888 &&\
mkdir /opt/notebooks && \
/opt/conda/bin/jupyter notebook \
    --config=/root/.ipython/profile_mynbs/ipython_notebook_config.py \
    --notebook-dir=/opt/notebooks \
    --no-browser
"
```

To get the password, check the logs of the container by running:

```
docker logs <CONTAINER_ID>
```

You will see an output like the following:

```
============================================================
Notebook config path: /root/.ipython/profile_hehe/
Notebook certificate path: /root
Notebook password: iEum7cCP
Notebook port: 8888
============================================================
```

#### Credentials

If you want to preset arguments instead of a default ones, you can set the following variables:

```
usage: cfg_notebook.py [-h] [-v] [-n CONFNAME] [-i PASSWORD] [-p PORT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -n CONFNAME, --confname CONFNAME
                        set ipython config folder name(default:mynbs)
  -i PASSWORD, --password PASSWORD
                        set ipython config folder name
  -p PORT, --port PORT  set ipython config folder name(default:mypass)
```

On this example we will preset our custom password:

```
$ docker run -d -p 8889:8889 xuhui546/anaconda-centos /bin/bash -c \
"python /root/cfg_notebook.py -p 8889 -i hello\
mkdir /opt/notebooks && \
/opt/conda/bin/jupyter notebook \
    --config=/root/.ipython/profile_mynbs/ipython_notebook_config.py \
    --notebook-dir=/opt/notebooks \
    --no-browser
"
```

## Copyright

Copyright (c) 2016 XuHui.
