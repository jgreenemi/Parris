# README #

![Parris Icon](/resources/Parris-Logo-Transparentx250.png)

Parris, the automated training tool for machine learning algorithms.

### Setup ###

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

### Roadmap ###

#### MVP ####

* Time-limit and cost-limit termination routines are implemented in the launched instance.

#### Iteration I ####

* Testing capabilities are implemented, so checks of the training routine are done before the instance is launched. (Catch failures early to save on costs from finding them after the instance has been launched.)
* IoT button integration with a demo Lambda function and trainer routine.
* IoT button is set up for public demo.

#### Iteration II ####

* .


### FAQ ###


### Contact ###

* Joseph Greene, jgreenemi@gmail.com

