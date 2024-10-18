from opn_api.api.base import ApiBase


class Export(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "export"
    """
    Haproxy ExportController
    """

    def config(self, *args):
        return self.api(*args, method="get", command="config")

    def diff(self, *args):
        return self.api(*args, method="get", command="diff")

    def download(self, *args):
        return self.api(*args, method="get", command="download")


class Service(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "service"
    """
    Haproxy ServiceController
    """

    def configtest(self, *args):
        return self.api(*args, method="get", command="configtest")

    def reconfigure(self, *args):
        return self.api(*args, method="post", command="reconfigure")


class Settings(ApiBase):
    MODULE = "haproxy"
    CONTROLLER = "settings"
    """
    Haproxy SettingsController
    """

    def add_acl(self, *args):
        return self.api(*args, method="post", command="addAcl")

    def add_action(self, *args):
        return self.api(*args, method="post", command="addAction")

    def add_backend(self, *args, body=None):
        return self.api(*args, method="post", command="addBackend", body=body)

    def add_cpu(self, *args):
        return self.api(*args, method="post", command="addCpu")

    def add_errorfile(self, *args):
        return self.api(*args, method="post", command="addErrorfile")

    def add_frontend(self, *args, body=None):
        return self.api(*args, method="post", command="addFrontend", body=body)

    def add_group(self, *args):
        return self.api(*args, method="post", command="addGroup")

    def add_healthcheck(self, *args):
        return self.api(*args, method="post", command="addHealthcheck")

    def add_lua(self, *args):
        return self.api(*args, method="post", command="addLua")

    def add_mapfile(self, *args):
        return self.api(*args, method="post", command="addMapfile")

    def add_server(self, *args, body=None):
        return self.api(*args, method="post", command="addServer", body=body)

    def add_user(self, *args):
        return self.api(*args, method="post", command="addUser")

    def add_mailer(self, *args):
        return self.api(*args, method="post", command="addmailer")

    def add_resolver(self, *args):
        return self.api(*args, method="post", command="addresolver")

    def del_acl(self, *args):
        return self.api(*args, method="post", command="delAcl")

    def del_action(self, *args):
        return self.api(*args, method="post", command="delAction")

    def del_backend(self, *args, body=None):
        return self.api(*args, method="post", command="delBackend", body=body)

    def del_cpu(self, *args):
        return self.api(*args, method="post", command="delCpu")

    def del_errorfile(self, *args):
        return self.api(*args, method="post", command="delErrorfile")

    def del_frontend(self, *args, body=None):
        return self.api(*args, method="post", command="delFrontend", body=body)

    def del_group(self, *args):
        return self.api(*args, method="post", command="delGroup")

    def del_healthcheck(self, *args):
        return self.api(*args, method="post", command="delHealthcheck")

    def del_lua(self, *args):
        return self.api(*args, method="post", command="delLua")

    def del_mapfile(self, *args):
        return self.api(*args, method="post", command="delMapfile")

    def del_server(self, *args):
        return self.api(*args, method="post", command="delServer")

    def del_user(self, *args):
        return self.api(*args, method="post", command="delUser")

    def del_mailer(self, *args):
        return self.api(*args, method="post", command="delmailer")

    def del_resolver(self, *args):
        return self.api(*args, method="post", command="delresolver")

    def get(self, *args):
        return self.api(*args, method="get", command="get")

    def set_acl(self, *args):
        return self.api(*args, method="post", command="setAcl")

    def set_action(self, *args):
        return self.api(*args, method="post", command="setAction")

    def set_backend(self, *args, body=None):
        return self.api(*args, method="post", command="setBackend", body=body)

    def set_cpu(self, *args):
        return self.api(*args, method="post", command="setCpu")

    def set_errorfile(self, *args):
        return self.api(*args, method="post", command="setErrorfile")

    def set_frontend(self, *args, body=None):
        return self.api(*args, method="post", command="setFrontend", body=body)

    def set_group(self, *args):
        return self.api(*args, method="post", command="setGroup")

    def set_healthcheck(self, *args):
        return self.api(*args, method="post", command="setHealthcheck")

    def set_lua(self, *args):
        return self.api(*args, method="post", command="setLua")

    def set_mapfile(self, *args):
        return self.api(*args, method="post", command="setMapfile")

    def set_server(self, *args, body=None):
        return self.api(*args, method="post", command="setServer", body=body)

    def set_user(self, *args):
        return self.api(*args, method="post", command="setUser")

    def set_mailer(self, *args):
        return self.api(*args, method="post", command="setmailer")

    def set_resolver(self, *args):
        return self.api(*args, method="post", command="setresolver")
