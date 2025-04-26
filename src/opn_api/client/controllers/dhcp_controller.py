from pydantic import ValidationError

from opn_api.api.core.dhcp_v4 import Leases as DhcpV4Leases, Service as DhcpV4Service
from opn_api.models.dhcp import DhcpLeaseResponse
from opn_api.exceptions import ParsingError

class DhcpLeaseController:
    """Controller for managing DHCPv4 Leases."""

    def __init__(self, client):
        """
        Initializes the DHCP Lease Controller.

        Args:
            client: The OPNsense API client instance.
        """
        self.dhcp_api = DhcpV4Leases(client)
        self.service_api = DhcpV4Service(client)

    def list_leases(self) -> DhcpLeaseResponse:
        """
        Lists current DHCP leases, optionally filtering and sorting.

        Returns:
            A DhcpLeaseResponse object containing the list of leases and pagination info.

        Raises:
            ParsingError: If the API response cannot be parsed.
            APIError: If the API call fails (assuming your client raises this).
        """
        api_response = self.dhcp_api.search_lease()
        try:
            return DhcpLeaseResponse.model_validate(api_response)
        except ValidationError as error:
            raise ParsingError(
                "Failed to parse DHCP lease list response",
                api_response,
                str(error),
            ) from error

    def delete_lease(self, address: str) -> dict:
        """
        Deletes a specific DHCP lease by IP address.
        Note: Deleting dynamic leases might be temporary until the client renews.
              This might primarily be for static leases depending on the backend API.

        Args:
            address: The IP address of the lease to delete.

        Returns:
            A dictionary containing the API response status.
        """
        return self.dhcp_api.del_lease(address)

    def apply_changes(self) -> dict:
        """Applies DHCP configuration changes."""
        return self.service_api.reconfigure()

