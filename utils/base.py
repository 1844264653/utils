from salmon.common.utils import local, remote
import random


class UtilsBase(object):

    def __init__(self, config=None, remote=True, platform='CentOS'):
        """

        :param config:
        :param remote:
        :param platform:
        :param os_type: linux | windows
        """
        self.config = config
        self.platform = platform
        self.os_type = config.get("os_type", "linux")
        if remote:
            self._init_remote_client(config=config)
            self.client = self.remote_client
        else:
            self._init_local_client(config=config)
            self.client = self.local_client

    def _init_remote_client(self, config=None):
        self.remote_client = None
        if config is not None:
            self.host = config.get("host")
            self.ssh_port = int(config.get("ssh_port", 22))

            self.ssh_username = config.get("ssh_username")
            self.ssh_password = config.get("ssh_password")
            self.connect_timeout = config.get("connect_timeout",300)
        if self.host is not None:
            self.remote_client = remote.Client(host=self.host,
                                               ssh_port=self.ssh_port,
                                               ssh_username=self.ssh_username,
                                               ssh_password=self.ssh_password,
                                               connect_timeout=self.connect_timeout)

    def _re_init_remote_client(self, config=None):
        if self.remote_client is not None:
            self.remote_client._close()
        self._init_remote_client(config=config)

    def _init_local_client(self, config=None):
        self.local_client = local.Client(config=config)

    @staticmethod
    def random_str(population=None, length=10):
        if population is None:
            population = "abcdefghijklmnopqrstuvwxyz0123456789"
        rand = random.sample(population, length)
        random_str = "".join(rand)
        return random_str
