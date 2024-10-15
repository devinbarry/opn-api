from opn_api.api.base import ApiBase


class Backup(ApiBase):
    MODULE = "backup"
    CONTROLLER = "backup"
    """
    api-backup BackupController
    """

    def download(self, *args):
        return self.api(*args, method="get", command="download")
