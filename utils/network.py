import re

from salmon.common.utils import base


class Utils(base.UtilsBase):

    def ping(self, host, count=10):
        # return like "3 packets transmitted, 3 received, 0% packet loss, time 1999ms"
        cmd = "ping %s -c %s | tail -2 | head -1" % (host, count)
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout

    def ping_ip(self, ip, count=10):
        cmd = "ping %s -c %s" % (ip, count)
        stdin, stdout, stderr = self.client.exec_command(cmd)
        pattern = re.compile(r"[0-9]{1,3}% packet loss", re.IGNORECASE)
        ret = pattern.findall(stdout.read())
        if ret == ['0% packet loss']:
            return {"ok": True, "loss_percent": "0%"}
        else:
            tmp = re.search("[0-9]{1,3}%", "".join(ret))
            loss_percent = tmp.group()
            return {"ok": False, "loss_percent": loss_percent}

    def ping_nslookup(self, domain_name):
        cmd = "ping %s -c 1 | sed -n '1p'" % domain_name
        stdin, stdout, stderr = self.client.exec_command(cmd)
        ret = stdout.read()
        tmp = re.search("([0-9]{1,3}\.){3}[0-9]{1,3}", ret)
        if tmp:
            ip = tmp.group()
        else:
            ip = None
        info = {
            "domain_name": domain_name,
            "ip": ip
        }
        return info

    def nslookup(self, domain_name):
        cmd = "nslookup %s | sed -n '4,5p'" % domain_name
        stdin, stdout, stderr = self.client.exec_command(cmd)

        lines = stdout.readlines()

        # lines = result.lines()
        domain_name_line_regx = "^Name:\s+%s" % domain_name
        ip_line_regx = "^Address\s+[0-9]+:\s+"
        info = {
            "domain_name": None,
            "ip": None,
        }

        # TODO : to support one domain_name map multi ips
        # TODO: the nslookup may not right depending on the the output of `nslookup`
        for line in lines:
            line = line.strip()
            line = re.sub("\n", "", line)

            if re.match(domain_name_line_regx, line):
                info["domain_name"] = domain_name
                continue
            if re.match(ip_line_regx, line):
                rets = re.split(ip_line_regx, line)
                if len(rets) != 2:
                    raise ValueError("Error occured when get the ip, the line is :%s" % line)
                info["ip"] = rets[-1]
            if info["domain_name"] is not None and info["ip"] is not None:
                break

        return info

    def get_network_info(self):
        if self.os_type == "windows":
            cmd = "ipconfig"
        else:
            cmd = "ip addr show"
        stdin, stdout, stderr = self.client.exec_command(cmd)
        addr_info = stdout.read()

        if self.os_type == "windows":
            addr_info = addr_info.decode("gbk")
        return addr_info
