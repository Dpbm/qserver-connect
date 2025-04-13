# Qserver Connect

A python library to help you connect with your [qserver](https://github.com/Dpbm/qserver) instance.

With this one, is easy to submit a job and retrieve its results after its execution.

## Installing

To install it, you must have installed:

* python >= 3.12
* pip/pip3
* a qserver instance running somewhere

ensuring that, you can run at your client machine:

```bash
pip install qserver-connect
```


## Usage

After installing, create a quantum circuit in your python framework of choice and then do the following:

1. Add a plugin to your backend(qserver)

If you haven't added any plugins to your server, you can use this very library to add. 
Here is a simple example of how does it work:

```python
from qserver_connect import Plugin
from qserver_connect.exceptions import FailedOnAddPlugin

# ... your code

# host = the ip/domain your instance is running
# http_port = by default the server exposes http as 8080 and https as 443, so add the one you want

# by default the plugin class uses https, so if you want to use http
# set secure_connection=False
plugin_manager = Plugin(host=host, port=http_port)

try:
    plugin_manager.add_plugin('plugin-name-you-want-to-add')
except FailedOnAddPlugin as error:
    # if there''s a problem with connection
    # or you already have added this plugin before
    # an error may be raised, so ensure you always
    # do exception handling    
    print(f"An error has occurred: {str(error)}")
```

2. submit your job

Then, you can submit the quantum circuit you've done and get the results.

To do that you can choose doing manually or allow the library to generate the data for you.

`Till this date (13/04/2025), the automatic job generation is only supported by Qiskit circuits.`

### Qiskit auto 

```python

from qserver_connect import Qiskit

# qc = your quantum circuit
# ... the remaining of your code


job = Qiskit(qc, {
    "backend" : # the backend you've chosen to use,
    "counts" : #set True if you want to retrieve the counts from this execution,
    "quasi_dist" : # set True if you want to retrieve the quasi_dist from this job,
    "expval": # set True if you want to retrieve expectation values from your circuit,
    "shots": # set the amount of shots you want. By default 1000 are taken. It's optional an only works when either "counts" or "quasi_dist" is/are True,
    "obs": # A list of Pauli Operators and coefficients following the qiskit pattern. It's required and only works when "expval" is True
})
```

### Manual

```python
from qserver_connect import Job

# First of all, you need to export your circuit to a .qasm file
# then run do:

job = Job({
    "qasm": #path to your qasm file,
    "counts": # True if you want to get counts from your circuit,
    "quasi_dist": # True if you want to get the quasi_dist from your circuit,
    "expval": # True if you want to get expectation values from your circuit,
    "simulator": # the target backend,
    "metadata": # the metadata must contain keys for shots (if you want a custom amount), and observables (when getting expval)
})

```

---

With your job object in hands, now you can, finally, submit your job and wait for the results. Here's a simple example of how could you do that:

```python
from time import sleep

from qserver_connect import JobConnection

# host = the host your backend is running
# http_port = the port for http/https
# grpc_port = the port to connect via grpc. By default, the backend runs the same as the http_port (8080 or 443), in case you've changed it, insert the new value here

# by default it also uses tls. So to used the unsecure version set: secure_connection=False
backend = JobConnection(host=host, http_port=http_port, grpc_port)

try:
    job_id = backend.send_job(job)
    
    while True:
        status = backend.get_job_data(job_id).get('status')

        if status is None:
            raise ValueError("Invalid status")

        print(f"Current status: {status}")

        if status not in ('pending', 'running'):
            break
        
        print("waiting job to finish")
        sleep(5)

    results = backend.get_job_result(job_id)
    print(results)

except Exception as error:
    print(f"Error: {str(error)}")
```

---

Available functions:


### Plugin

| method | parameters | returns |
|--------|------------|---------|
|add_plugin|name:str  | -       |
|delete_plugin|name:str | -     |

### JobConnection


| method | parameters | returns |
|--------|------------|---------|
|send_job|job_data:Job| the job id (str) |
|get_job_data|job_id:str|the json response (dict) |
|get_job_result|job_id:str|the json response (dict) |
|get_all_jobs|cursor:Optional[int] | the paginated jobs list (List[dict]) |
|delete_job|job_id:str|-|


## Dev usage

### Testing

For tests, you must have:

* qserver running
* conda/pip(3)
* python >= 3.12

First, to run the tests, you must install the dependencies. You can use the pure pip installation, or use conda/conda-lock to start.

```bash
# with pip
pip install -r requirements.txt -r dev-requirements.txt

# using conda based env
conda env create -f environment.yml
mamba env create -f environment.yml
conda-lock install -n qserver-connect conda-lock.yml

# remember to activate your environment
```

Then, run the tests with:

```bash
HOST="the-backend-host" tox
```

### Get newest proto definition

Once we are using grpc/protobuf to handle jobs, we need to ensure we're using the latest definition.

It's not required to run it every time, but if you notice any major change in [qserver](https://github.com/Dpbm/qserver), run:

```bash
# ensure you have installed everything and, if you've chosen to use a virtual env,
# the env is activated 

chmod +x get-proto-from-server.sh && ./get-proto-from-server.sh
```

### Contributing

Feel free to open issues and PRs adding, updating, removing and requesting features you would like to see in this project.