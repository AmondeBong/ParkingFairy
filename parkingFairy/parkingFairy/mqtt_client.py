import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        # 연결이 성공했을 때 수행할 동작을 추가합니다.
        # 예: 토픽 구독, 메시지 발행 등
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, msg):
    # 메시지 수신 시 동작을 추가합니다.
    pass


def mqtt_connect():
    # MQTT 브로커에 연결하는 함수입니다.
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    broker_address = "mqtt.example.com"
    port = 1883  # MQTT 브로커 포트 (기본값: 1883)

    client.connect(broker_address, port=port, keepalive=60)
    client.loop_start()  # MQTT 클라이언트를 시작합니다.
    return client
