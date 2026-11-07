from machine import Pin, time_pulse_us
import network
from umqtt.simple import MQTTClient
import time
import ujson

# Configurazione posto
ID_POSTO = "A-101"
SOGLIA_CM = 50

# Configurazione MQTT
MQTT_BROKER = "broker.emqx.io" 
MQTT_TOPIC = "parking/spots/" + ID_POSTO

# Configurazione dei pin
trigger = Pin(5, Pin.OUT)
eco = Pin(18, Pin.IN)

led_verde = Pin(19, Pin.OUT)
led_rosso = Pin(21, Pin.OUT)


def connetti_wifi():
    print("Connessione al WiFi...", end="")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Wokwi-GUEST", "")
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")
    print(" Connesso!")

def misura_distanza():
    # Assicura che il trigg sia basso
    trigger.value(0)
    time.sleep_us(2)

    # invia un impulso di 10 microsecondi sul pin
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    # Legge la durata dell'impulso HIGH sul pin ECHO (timeout 30ms)
    durata = time_pulse_us(eco, 1, 30000)

    if durata < 0:
        return None
        
        
    # Velocità del suono: ~0.0343 cm/us (diviso 2 per andata e ritorno)
    distanza = (durata * 0.0343) / 2
    return round(distanza)


def aggiorna_led(occupato):
    if occupato:
        led_rosso.value(1)
        led_verde.value(0)
    else:
        led_rosso.value(0)
        led_verde.value(1)


# Avvio del programma
print("=== Avvio sensore parcheggio intelligente:", ID_POSTO, "===")

connetti_wifi()

# Connessione al broker MQTT
client = MQTTClient("esp32_" + ID_POSTO, MQTT_BROKER)
client.connect()
print("Connesso al Broker MQTT!")

while True:

    distanza = misura_distanza()

    if distanza is not None:

        # Determina se il posto è occupato
        occupato = distanza < SOGLIA_CM

        # Aggiorna i LED
        aggiorna_led(occupato)

        # Prepara i dati da mandare al backend
        dati = {
            "id": ID_POSTO,
            "distanza_cm": distanza,
            "occupato": occupato
        }
        
        messaggio_json = ujson.dumps(dati)

        # Stampa i dati in formato JSON
        print("Lettura valida:", ujson.dumps(dati))
        # Invio dati broker MQTT
        client.publish(MQTT_TOPIC, messaggio_json)

    else:
        print("Errore nella lettura del sensore")

    # Attende 2 secondi prima della prossima misurazione
    time.sleep(2)
