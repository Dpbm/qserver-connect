from http import HTTPStatus
import logging
import requests as req
from .url import URL, HTTP
from .exceptions import FailedOnAddPlugin, FailedOnDeletePlugin
from .constants import TIMEOUT_TIME

logger = logging.getLogger(__name__)


class Plugin:
    """
    A class to interact with the API to get and send information about plugins/backends.
    """

    def __init__(self, host: str, port: int, secure_connection: bool = True):
        """
        Setup API data.
        """

        self._host = host
        self._port = port
        self._secure = secure_connection
        self._url_handler = URL(self._host, self._port, http=HTTP(secure_connection))

    def add_plugin(self, name: str):
        """
        Gets a plugin name as input and try to add it on the server.
        """

        url = self._url_handler.get_add_plugin_url(name)

        status_code = int(HTTPStatus.BAD_REQUEST)

        try:
            result = req.post(url, timeout=TIMEOUT_TIME)
            status_code = result.status_code

        except Exception as error:
            logger.error("Failed on add plugin")
            logger.error(str(error))
            raise FailedOnAddPlugin(name) from error

        if status_code != HTTPStatus.CREATED:
            raise FailedOnAddPlugin(name)

    def delete_plugin(self, name: str):
        """
        Try to delete a plugin on backend.
        """

        url = self._url_handler.get_delete_plugin_url(name)
        status_code = int(HTTPStatus.BAD_REQUEST)

        try:
            result = req.delete(url, timeout=TIMEOUT_TIME)
            status_code = result.status_code

        except Exception as error:
            logger.error("Failed on remove your plugin.")
            logger.error(str(error))
            raise FailedOnDeletePlugin(name) from error

        if status_code != HTTPStatus.OK:
            raise FailedOnDeletePlugin(name)
