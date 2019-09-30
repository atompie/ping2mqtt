import time
import logging
import multiping
from multiping import multi_ping


class PingPong:

    def __init__(self, conf, logger):

        self.config = conf
        self.logger = logger

        addresses = self.config.sections()
        if 'ping' in addresses:
            del addresses[addresses.index('ping')]
        if 'mqtt' in addresses:
            del addresses[addresses.index('mqtt')]

        self.interval = int(self.config['ping'].get('interval', 30))
        self.timeout = int(self.config['ping'].get('timeout', 2))
        self.retry = int(self.config['ping'].get('retry', 3))
        self.addresses = addresses
        self.update_time = int(self.config['ping'].get('update_time', 600))
        self.ping_state = {addr: None for addr in addresses}
        self.last_update = 0
        self.logger.info("Interval: {}".format(self.interval))
        self.logger.info("Addresses: {}".format(self.addresses))
        self.logger.info("Timeout: {}".format(self.timeout))
        self.logger.info("Retry: {}".format(self.retry))

    def _get_topic(self, ip):
        prefix = self.config[ip].get('prefix', 'ping')
        return self.config[ip]['topic'].replace('$prefix', prefix)

    def _time_to_update(self):
        timestamp = time.time()
        return self.last_update + self.update_time <= timestamp

    def __iter__(self):
        while True:
            try:
                online, offline = multi_ping(self.addresses, self.timeout, self.retry)

                if self._time_to_update():
                    self.ping_state = {addr: None for addr in self.addresses}
                    self.last_update = time.time()

                for ip, response_time in online.items():
                    online_payload = self.config[ip]['online_payload'] if 'online_payload' in self.config[
                        ip] else response_time

                    qos = int(self.config[ip].get('qos',0))

                    if self.ping_state[ip] != online_payload:
                        self.ping_state[ip] = online_payload

                        yield self._get_topic(ip), online_payload, qos

                for ip in offline:
                    offline_payload = self.config[ip]['offline_payload'] if 'offline_payload' in self.config[
                        ip] else -1

                    qos = int(self.config[ip].get('qos', 0))

                    if self.ping_state[ip] != offline_payload:
                        self.ping_state[ip] = offline_payload

                        yield self._get_topic(ip), offline_payload, qos

                time.sleep(self.interval)

            except multiping.MultiPingSocketError as e:
                logging.error(str(e))

            except OSError as e:
                logging.error(str(e))

