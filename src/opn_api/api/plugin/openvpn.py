from opn_api.api.base import ApiBase


class Openvpn(ApiBase):
    MODULE = "openvpn"
    CONTROLLER = "export"
    """
    OPENVPN EXPORT
    """

    def accounts(self, *args):
        return self.api(*args, method="get", command="accounts")

    def download(self, *args, json=None):
        return self.api(*args, method="post", command="download", json=json)

    def providers(self, *args):
        return self.api(*args, method="get", command="providers")

    def templates(self, *args):
        return self.api(*args, method="get", command="templates")
