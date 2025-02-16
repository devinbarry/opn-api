from opn_api.api.base import ApiBase


class Tunnel(ApiBase):
    """
    Ipsec TunnelController
    """

    MODULE = "ipsec"
    CONTROLLER = "tunnel"

    def search_phase1(self, *args):
        return self.api(*args, method="get", command="searchPhase1")

    def search_phase2(self, *args):
        return self.api(*args, method="post", command="searchPhase2")
