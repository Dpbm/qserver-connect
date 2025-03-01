from typing import Optional

def get_method(url:str, jobId:Optional[str]):
    if(not isinstance(jobId, str)):
        raise ValueError("Your JobId is invalid!")
    
    return f"http://{url}/api/job/{jobId}"

def add_method(url:str, _:Optional[str]):
    return f"{url}/"

methods = {
    "add": add_method,
    "get": get_method
}

def get_url(url:str, method:str, job_id:Optional[str]=None) -> str:
    method_url_creation_func = methods.get(method)

    if(method_url_creation_func is None):
        raise ValueError("Invalid method!")

    return method_url_creation_func(url, job_id)