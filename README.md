# README #

![Parris Icon](/resources/Parris-Logo-Transparentx250.png)

Parris, the automated training tool for machine learning algorithms.

## ##

## Setup ##

You'll need an AWS account, AWS credentials loaded to your workstation (set up through `$ aws configure`), a machine learning algorithm to train, and of course a dataset that it can be trained on. You'll also likely want an S3 bucket or some other storage location for your algorithm's training results.

UNIX/Linux:
```bash
$ git clone https://github.com/jgreenemi/parris.git && cd parris
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip --version
pip 9.0.1 from ...\python\python36\lib\site-packages (python 3.6)
(env) $ pip install -r requirements.txt 
```

Windows:
```bash
$ git clone https://github.com/jgreenemi/parris.git && cd parris
$ virtualenv -p python3.exe env
$ env/Scripts/activate
(env) $ pip --version
pip 9.0.1 from ...\python\python36\lib\site-packages (python 3.6)
(env) $ pip install -r requirements.txt 
```

### FAQ ###

Consult the [FAQ page in the documentation](/docs/FAQ.md) as many questions are answered there. If your question was not answered, please get in touch, either via a new Github Issue (preferred) or via an email below. The former is preferred as others with the same question can benefit from seeing the answer posted publicly.

### Contact ###

* Joseph Greene, jgreenemi@gmail.com

