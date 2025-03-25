from qserver_connect import JobConnection, Plugin


class TestPlugins:
    """
    Test plugins functionalities
    """

    def test_add_plugin(self, connection, plugin_name):
        """Test wether a plugin can be added"""
        host, port_http, _ = connection

        p = Plugin(host=host, port=port_http, secure_connection=False)
        p.add_plugin(plugin_name)

    def test_remove_plugin(self, connection, plugin_name):
        """Test wether a plugin can be deleted"""
        host, port_http, _ = connection

        p = Plugin(host=host, port=port_http, secure_connection=False)
        p.add_plugin(plugin_name)
        p.delete_plugin(plugin_name)

    def test_delete_plugin_when_job_is_running(
        self, connection, plugin_name, long_job_data
    ):
        """Test wether a plugin can be deleted during execution"""

        host, port_http, port_grpc = connection

        p = Plugin(host=host, port=port_http, secure_connection=False)
        j = JobConnection(
            host=host, http_port=port_http, grpc_port=port_grpc, secure_connection=False
        )

        p.add_plugin(plugin_name)
        j.send_job(long_job_data)
        p.delete_plugin(plugin_name)
