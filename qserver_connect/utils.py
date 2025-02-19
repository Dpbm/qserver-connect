from typing import Optional

def get_method(jobId:Optional[str]):
    if(not isinstance(jobId, str)):
        raise ValueError("Your JobId is invalid!")
    
    return f"/api/job/{jobId}"


methods = {
    "add": lambda _ : "/",
    "get": get_method
}

def get_url(url:str, method:str, job_id:Optional[str]=None) -> str:
    method_path_creation_func = methods.get(method)

    if(method_path_creation_func is None):
        raise ValueError("Invalid method!")

    method_path = method_path_creation_func(job_id)

    return f"{url}{method_path}"
