from opn_api.api.base import ApiBase


class Leases4(ApiBase):
    """
    DHCP Leases4Controller - DO NOT USE
    This controller is documented, but endpoints are not implemented in the API.
    """

    MODULE = "dhcp"
    CONTROLLER = "leases4"

    def del_lease(self, ip, *args):
        """
        Delete a DHCPv4 lease by IP address.

        Args:
            ip (str): The IP address of the lease to delete.
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response.
        """
        # Assuming the IP is passed as part of the URL path after the command.
        return self.api(ip, *args, method="post", command="delLease")

    def search_lease(self, *args):
        """
        Search for DHCPv4 leases.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response containing search results.
        """
        return self.api(*args, method="get", command="searchLease")


class Service(ApiBase):
    """
    DHCP ServiceController
    """

    MODULE = "dhcp"
    CONTROLLER = "service"

    def restart(self, *args):
        """
        Restart the DHCP service.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response.
        """
        return self.api(*args, method="post", command="restart")

    def start(self, *args):
        """
        Start the DHCP service.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response.
        """
        return self.api(*args, method="post", command="start")

    def status(self, *args):
        """
        Get the status of the DHCP service.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response containing the service status.
        """
        return self.api(*args, method="get", command="status")

    def stop(self, *args):
        """
        Stop the DHCP service.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response.
        """
        return self.api(*args, method="post", command="stop")
