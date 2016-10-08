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
$ docker run -d -p 8888:8888 xuhui546/anaconda-centos
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

#### Custom

If you want to preset arguments instead of a default ones, you can set the following variables:

```
optional arguments:
  -e "JUPYTER_NAME=nbs"            set jupyter config folder name(default:mynbs)
  -e "JUPYTER_PORT=88"             set jupyter server listen port(default:8888)
  -e "JUPYTER_PASS=mypass"         set jupyter login password(default:random)
  -e "JUPYTER_WORKDIR=/root"       set jupyter workdir(default:/)
```

On this example we will preset our custom password:

```
$ docker run -d -p 8889:88 -e "JUPYTER_NAME=nbs" -e "JUPYTER_PORT=88" \
-e "JUPYTER_PASS=mypass" -e "JUPYTER_WORKDIR=/root" xuhui546/anaconda-centos
```

## Copyright

Copyright (c) 2016 XuHui.
