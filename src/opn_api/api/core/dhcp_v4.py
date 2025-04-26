from opn_api.api.base import ApiBase


class Leases(ApiBase):
    """
    DHCPv4 LeasesController
    """

    MODULE = "dhcpv4"
    CONTROLLER = "leases"

    def del_lease(self, ip, *args):
        """
        Delete a DHCP lease by IP address.

        Args:
            ip (str): The IP address of the lease to delete.
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response.
        """
        # Assuming the IP is passed as part of the URL path after the command,
        # similar to how UUIDs are often handled in other modules.
        return self.api(ip, *args, method="post", command="delLease")

    def search_lease(self, *args):
        """
        Search for DHCP leases.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response containing search results.
        """
        return self.api(*args, method="get", command="searchLease")


class Service(ApiBase):
    """
    DHCPv4 ServiceController
    """

    MODULE = "dhcpv4"
    CONTROLLER = "service"

    def reconfigure(self, *args):
        """
        Reconfigure the DHCP service.

        Args:
            *args: Additional arguments to pass to the API call.

        Returns:
            dict: API response.
        """
        return self.api(*args, method="post", command="reconfigure")

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
