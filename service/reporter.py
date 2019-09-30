from service.mqtt.client import MqttSubscriber, MqttClient


class Update:
    def __init__(self):
        self._require_update = False

    def update(self):
        self._require_update = True

    def reset(self):
        self._require_update = False

    def __bool__(self):
        return self._require_update


class MqttReporter:

    def __init__(self, server: str, port: int, credentials: tuple, logger=None):
        self.logger = logger
        user, password = credentials
        self._prefix = 'ping'
        self._mqtt_client = MqttClient(
            server=server, user=user, password=password, port=port,
            logger=logger,
            subscribe=MqttSubscriber(topic="{}/CMND".format(self._prefix), callback=self._on_cmnd)
        )

        self.require_update = Update()

    def _on_cmnd(self, client, userdata, msg):
        if msg.payload.lower() == b'update':
            self.require_update.update()

    def report(self, topic, payload, qos):
        self.require_update.reset()
        return self._mqtt_client.publish(topic, payload, qos)
