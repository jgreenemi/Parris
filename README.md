# README #

![Parris Icon](/resources/Parris-Logo-Transparentx250.png)

Parris, the automated training tool for machine learning algorithms.

## What Is This Tool? ##

Parris is a tool for automating the training of machine learning algorithms. If you're the kind of person that works on ML algorithms and spends too much time setting up a server to run it on, having to log into it to monitor its progress, etc., then you will find this tool helpful. No need to SSH into instances to get your training jobs done!

## Setup ##

You'll need an AWS account, AWS credentials loaded to your workstation (set up through `$ aws configure`), a machine learning algorithm to train, and of course a dataset that it can be trained on. You'll also likely want an S3 bucket or some other storage location for your algorithm's training results.

UNIX/Linux:
```bash
$ git clone https://github.com/jgreenemi/parris.git && cd parris
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip --version
pip 9.0.1 from .../env/lib/python3.6/site-packages (python 3.6)
(env) $ pip install -r requirements.txt 
```

Windows:
```bash
$ git clone https://github.com/jgreenemi/parris.git && cd parris
$ virtualenv -p python3.exe env
$ env\Scripts\activate
(env) $ pip --version
pip 9.0.1 from ...\python\python36\lib\site-packages (python 3.6)
(env) $ pip install -r requirements.txt 
```

## How To Use ##

To use Parris, follow the [Getting Started guide](/docs/GETTING-STARTED.md) which will take you from setup all the way to launching your first ML training stack. While getting familiar with the tool you'll also want to [consult the Configuration guide](/docs/CONFIGURATION.md) to better understand what options are available to you. This will help a lot in conjunction with the Getting Started guide.

## FAQ ##

Consult the [FAQ page in the documentation](/docs/FAQ.md) as many questions are answered there. If your question was not answered, please get in touch, either via a new Github Issue (preferred) or via an email below. The former is preferred as others with the same question can benefit from seeing the answer posted publicly.

## Contact ##

* Joseph Greene, [jgreenemi@gmail.com](mailto:jgreenemi@gmail.com)

