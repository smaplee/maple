import json
from lib.cmd import stdout


class SYS(object):

    def __init__(self):
        self.cpuvalue = self.cpuinfo()
        self.mem = self.meminfo()
        self.osvalue = self.osinfo()

    @property
    def cpu(self):
        return self.cpuvalue['model name']

    @property
    def cores(self):
        if self.cpuvalue.has_key('cpu cores'):
            return self.cpuvalue['cpu cores']
        else:
            return 2**int(self.cpuvalue['processor'])

    @property
    def hostname(self):
        return self.osvalue['hostname']

    @property
    def os(self):
        return self.osvalue['type']

    @property
    def kernel(self):
        return self.osvalue['kernel']

    @property
    def disk(self):
        return self.diskinfo()

    @property
    def memory(self):
        # available = self.mem['MemFree'] + self.mem['Buffers'] + self.mem['Cached']
        total = self.mem['MemTotal']
        return total

    def __repr__(self):
        return json.dumps({'hostname': self.hostname, 'os': self.os, 'kernel': self.kernel, 'cpu': self.cpu, 'cores': self.cores, 'disk':  self.disk, 'mem': self.memory})

    def __str__(self):
        return json.dumps({'hostname': self.hostname, 'os': self.os, 'kernel': self.kernel, 'cpu': self.cpu, 'cores': self.cores, 'disk':  self.disk, 'mem': self.memory})

    def cpuinfo(self):
        cpu = {}
        with open('/proc/cpuinfo') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if len(line.split(':')) > 1:
                    key, value = line.split(':')
                    cpu[key.strip()] = value.strip().strip('KB')
        return cpu

    def osinfo(self):
        os = {}
        _, result = stdout('uname -a')
        info = result.split()
        os['type'] = info[0]
        os['hostname'] = info[1]
        os['kernel'] = info[2]
        return os

    def meminfo(self):
        mem = {}
        with open('/proc/meminfo') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                key, value = line.split(':')
                mem[key.strip()] = value.strip().strip('kB')
        return mem

    def diskinfo(self):
        disk = []
        with open('/proc/partitions') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if re.match('^[0-9].*[a-z]$', line):
                    _, _, blocks, name = line.split()
                    info = '%s: %sG' % (name, float(blocks)/1024/1024)
                    disk.append(info)
        return ','.join(disk)

    @property
    def iface(self):
        with open('/proc/net/route') as f:
            for line in f:
                net = line.split()
                if net[3] == '0003':
                    iface = net[0]
                    return iface
        return None

    def serialize(self):
        return json.dumps({'hostname': self.hostname, 'os': self.os, 'kernel': self.kernel, 'cpu': self.cpu, 'cores': self.cores, 'disk':  self.disk, 'mem': self.memory, 'iface': self.iface})