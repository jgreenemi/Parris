# README #

![Parris Icon](/resources/Parris-Logo-Transparentx400.png)

Parris, the automated training tool for machine learning algorithms.

### Setup ###

You'll need an AWS account.


```bash
$ git clone https://*/parris.git && cd parris
$ virtualenv -p python3 env
$ source env/bin/activate
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

