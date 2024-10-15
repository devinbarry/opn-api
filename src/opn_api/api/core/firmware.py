from opn_api.api.base import ApiBase


class Firmware(ApiBase):
    MODULE = "Core"
    CONTROLLER = "Firmware"

    def info(self, *args):
        return self.api(*args, method="get", command="info")

    def upgrade_status(self, *args):
        return self.api(*args, method="get", command="upgradestatus")

    def install(self, *args):
        return self.api(*args, method="post", command="install")

    def reinstall(self, *args):
        return self.api(*args, method="post", command="reinstall")

    def remove(self, *args):
        return self.api(*args, method="post", command="remove")

    def lock(self, *args):
        return self.api(*args, method="post", command="lock")

    def unlock(self, *args):
        return self.api(*args, method="post", command="unlock")

    def details(self, *args):
        return self.api(*args, method="post", command="details")
