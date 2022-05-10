# rasa 3.1 is used

CMPE252, Xichang Yu

1. install rasa.
https://rasa.com/docs/rasa/installation/

2. install mysql.
https://dev.mysql.com/downloads/installer/

3. install mysql connector for python 
https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html

4. Clone/download this repo

5. set up database by importing schema and tables from 'sql' folder.

6. Cd to this rasa folder

7. 'rasa run actions' to start the action server

8. 'Rasa shell' to start the chatbot shell

9. 'Rasa run' to rerun the chatbot as a service.

Optional: follow this guide to deploy rasa on slack. You might need 'ngrok' to forward your local port
https://rasa.com/docs/rasa/connectors/slack/


Recommended story line:
*check demo_history.doc to see the expected conversations.

- story: find restaurants 1
  steps:
  - intent: greet
  - action: utter_greet
  - intent: look_for_restaurants
  - action: utter_ask_location
  - intent: tell_location
    entities:
    - location: "San Francisco"
  - action: utter_ask_food
  - intent: tell_food
    entities:
    - food_type: "Taco"
  - action: action_check_restaurants
  - intent: ask_restaurant_detail
    entities:
    - restaurant_name: "Virrueta’s Tacos"
  - action: action_restaurant_detail
  - action: utter_ask_send_email
  - intent: affirm
  - action: action_ask_if_email
  - intent: tell_name
    entities:
    - name: "Jon"
  - action: utter_ask_email2
  - intent: tell_email
    entities: 
    - email: "qwerrty32@gmail.com"
  - action: action_save_id
  - action: action_send_email
  - action: utter_thanks


BUGS:
Try to follow the stoylines. restarting the shell/run service is the best way when encounter bugs.


* Below is the env that was tested working. You can check if there is any package missing.
pip freeze list:

absl-py==0.13.0

aio-pika==6.8.2

aiofiles==0.8.0

aiohttp==3.7.4

aiormq==3.3.1

APScheduler==3.7.0

astunparse==1.6.3

async-generator==1.10

async-timeout==3.0.1

attrs==21.2.0

bidict==0.22.0

boto3==1.21.46

botocore==1.24.46

CacheControl==0.12.11

cachetools==4.2.4

certifi==2021.10.8

cffi==1.15.0

chardet==3.0.4

charset-normalizer==2.0.12

cloudpickle==1.6.0

colorclass==2.2.2

coloredlogs==15.0.1

colorhash==1.0.4

cryptography==3.4.8

cycler==0.11.0

dask==2021.11.2

dnspython==1.16.0

docopt==0.6.2

fbmessenger==6.0.0

fire==0.4.0

flatbuffers==2.0

fsspec==2022.3.0

future==0.18.2

gast==0.4.0

google-auth==1.35.0

google-auth-oauthlib==0.4.6

google-pasta==0.2.0

greenlet==1.1.2

grpcio==1.44.0

h5py==3.6.0

httptools==0.4.0

humanfriendly==10.0

idna==3.3

importlib-metadata==4.11.3

jmespath==1.0.0

joblib==1.0.1

jsonpickle==2.0.0

jsonschema==3.2.0

kafka-python==2.0.2

keras==2.7.0

Keras-Preprocessing==1.1.2

kiwisolver==1.4.2

libclang==14.0.1

locket==1.0.0

Markdown==3.3.6

matplotlib==3.3.4

mattermostwrapper==2.2

msgpack==1.0.3

multidict==5.2.0

mysql-connector-python==8.0.29

networkx==2.6.3

numpy==1.19.5

oauthlib==3.2.0

opt-einsum==3.3.0

packaging==20.9

pamqp==2.3.0

partd==1.2.0

Pillow==9.1.0

prompt-toolkit==2.0.10

protobuf==3.20.1

psycopg2-binary==2.9.3

pyasn1==0.4.8

pyasn1-modules==0.2.8

pycparser==2.21

pydot==1.4.2

PyJWT==2.1.0

pykwalify==1.8.0

pymongo==3.10.1

pyparsing==3.0.8

pyrsistent==0.18.1

pyTelegramBotAPI==3.8.3

python-crfsuite==0.9.8

python-dateutil==2.8.2

python-engineio==4.3.2


python-socketio==5.6.0

pytz==2021.3

PyYAML==6.0

questionary==1.10.0

randomname==0.1.5

rasa==3.1.0

rasa-sdk==3.1.1

redis==3.5.3

regex==2021.8.28

requests==2.27.1

requests-oauthlib==1.3.1

requests-toolbelt==0.9.1

rocketchat-API==1.16.0

rsa==4.8

ruamel.yaml==0.16.13

ruamel.yaml.clib==0.2.6

s3transfer==0.5.2

sanic==21.12.1

Sanic-Cors==2.0.1

sanic-jwt==1.7.0

sanic-routing==0.7.2

scikit-learn==0.24.2

scipy==1.8.0

sentry-sdk==1.3.1

six==1.16.0

sklearn-crfsuite==0.3.6

slackclient==2.9.4

SQLAlchemy==1.4.35

tabulate==0.8.9

tarsafe==0.0.3

tensorboard==2.8.0

tensorboard-data-server==0.6.1

tensorboard-plugin-wit==1.8.1

tensorflow==2.7.1

tensorflow-addons==0.15.0

tensorflow-estimator==2.7.0

tensorflow-hub==0.12.0

tensorflow-io-gcs-filesystem==0.25.0

tensorflow-text==2.7.3

termcolor==1.1.0

terminaltables==3.1.10

threadpoolctl==3.1.0

toolz==0.11.2

tqdm==4.64.0

twilio==6.50.1

typeguard==2.13.3

typing-extensions==3.10.0.2

typing-utils==0.1.0

tzlocal==2.1

ujson==4.3.0

urllib3==1.26.9

uvloop==0.16.0

wcwidth==0.2.5

webexteamssdk==1.6

websockets==10.3

Werkzeug==2.1.1

wrapt==1.14.0

yarl==1.7.2

zipp==3.8.0



