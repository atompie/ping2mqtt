from service.mqtt.client import MqttSubscriber, MqttClient


class MqttReporter:

    def __init__(self, server: str, port: int, credentials: tuple):
        user, password = credentials
        self._prefix = 'ping'
        self._mqtt_client = MqttClient(
            server=server, user=user, password=password, port=port,
            subscribe=MqttSubscriber(topic="{}/CMND".format(self._prefix), callback=self._on_cmnd)
        )

        self.require_update = False

    def _on_cmnd(self, client, userdata, msg):
        if msg.payload.lower() == b'update':
            self.require_update = True

    def report(self, topic, payload, qos):
        return self._mqtt_client.publish(topic, payload, qos)
