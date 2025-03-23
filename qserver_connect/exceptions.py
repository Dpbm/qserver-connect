class FailedOnGetJobResult(Exception):
    """
    Exception for when an error has occoured during the retrieving of your job results.
    """

    def __init__(self):
        super().__init__("Failed on get your job resuts!")


class FailedOnGetJobData(Exception):
    """
    Exception for when an error has occoured during the retrieving of your job data.
    """

    def __init__(self):
        super().__init__("Failed on get your job data!")


class JobNotFound(Exception):
    """
    Exception for when your job id wasn't found.
    """

    def __init__(self, job_id: str):
        super().__init__(f"Job not found with id: {job_id}")


class FailedOnAddPlugin(Exception):
    """
    Exception for when an error has occoured during adding a plugin.
    """

    def __init__(self, plugin_name: str):
        super().__init__(f"Failed on Add Plugin: {plugin_name}")


class FailedOnDeletePlugin(Exception):
    """
    Exception for when an error has occoured during deleting a plugin.
    """

    def __init__(self, plugin_name: str):
        super().__init__(f"Failed on Delete Plugin: {plugin_name}")


class InvalidObservables(Exception):
    """
    Exception for when an invalid Observable was provided.
    """

    def __init__(self):
        super().__init__(
            "You must provide observables when retrieving Expectation values"
        )


class InvalidResultTypes(Exception):
    """
    Exception for when no Result types were provided.
    """

    def __init__(self):
        super().__init__("You must select at least one type of result")


class FailedOnCreateJob(Exception):
    """
    Exception for when an error occoured on creating a job.
    """

    def __init__(self):
        super().__init__(
            "It wasn't possible to create your job.\n"
            + "Make sure your data is correct!\n"
            + "Remember to add measurements on your circuit "
            + "in case you want to extract quasi dist or counts"
        )


class QiskitError(Exception):
    """
    Handles errors from qiskit import.
    """

    def __init__(self):
        super().__init__(
            "It wasn't possible to import a qiskit functionality.\n"
            + "It probably means you're using a different version of qiskit.\n"
            + "Make sure the installed version is >=1.3.2 or "
            + "Create your job manually using the `JobConnection` class."
        )
