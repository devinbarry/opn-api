from opn_api.api.base import ApiBase


class Backup(ApiBase):
    MODULE = "core"
    CONTROLLER = "backup"
    """
    api-backup BackupController
    """

    @ApiBase._api_call
    def download(self, *args):
        self.method = "get"
        self.command = "download"
