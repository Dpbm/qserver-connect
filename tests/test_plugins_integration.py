from qserver_connect import Plugin


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

    def test_plugin_https(self, connection_secure, plugin_name):
        """Should add and remove a plugin with no problems with secure connection"""
        host, port_https, _ = connection_secure
        p = Plugin(host=host, port=port_https, secure_connection=True)
        p.add_plugin(plugin_name)
        p.delete_plugin(plugin_name)
