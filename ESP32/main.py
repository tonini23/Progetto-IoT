from machine import Pin, time_pulse_us, I2C
import network
from umqtt.simple import MQTTClient
import time
import ujson
import ssd1306  


POSTI = [
    {"id": "A-101", "trigger": Pin(5, Pin.OUT), "echo": Pin(18, Pin.IN), "soglia": 50},
    {"id": "A-102", "trigger": Pin(4, Pin.OUT), "echo": Pin(19, Pin.IN), "soglia": 50},
    {"id": "A-107", "trigger": Pin(22, Pin.OUT), "echo": Pin(23, Pin.IN), "soglia": 50},
    {"id": "B-116", "trigger": Pin(32, Pin.OUT), "echo": Pin(33, Pin.IN), "soglia": 50},
]

# Configurazione MQTT
MQTT_BROKER = "broker.emqx.io"

# LED di stato generali 
led_verde = Pin(12, Pin.OUT)
led_rosso = Pin(14, Pin.OUT)

# Inizializzazione Display OLED I2C (SCL=22, SDA=21)
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display_width = 128
display_height = 64
oled = ssd1306.SSD1306_I2C(display_width, display_height, i2c)

def connetti_wifi():
    print("Connessione al WiFi...", end="")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Wokwi-GUEST", "")
    while not wlan.isconnected():
        time.sleep(0.5)
        print(".", end="")
    print(" Connesso!")

def misura_distanza(trigger, eco):
    trigger.value(0)
    time.sleep_us(2)

    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)
    
    durata = time_pulse_us(eco, 1, 30000)

    if durata < 0:
        return None
        
    distanza = (durata * 0.0343) / 2
    return round(distanza)

def aggiorna_display(id_posto, distanza, occupato):
    oled.fill(0)  # Pulisce lo schermo
    
    # Scrive le informazioni sullo schermo OLED
    oled.text(f"Posto: {id_posto}", 0, 0)
    oled.text(f"Distanza: {distanza} cm", 0, 20)
    
    stato_str = "OCCUPATO" if occupato else "LIBERO"
    oled.text(f"Stato: {stato_str}", 0, 40)
    
    oled.mostra()  # Aggiorna il display fisico

# Avvio del programma
print("=== Avvio sistema Smart Parking a 4 Posti con OLED ===")
connetti_wifi()

# Connessione al broker MQTT
client = MQTTClient("esp32_multi_parking", MQTT_BROKER)
client.connect()
print("Connesso al Broker MQTT!")

while True:
    for posto in POSTI:
        distanza = misura_distanza(posto["trigger"], posto["echo"])

        if distanza is not None:
            occupato = distanza < posto["soglia"]

            dati = {
                "id": posto["id"],
                "distanza_cm": distanza,
                "occupato": occupato
            }
            
            messaggio_json = ujson.dumps(dati)
            topic = f"parking/spots/{posto['id']}"

            print(f"Lettura valida [{posto['id']}]:", messaggio_json)
            
            # Pubblica i dati sul broker MQTT
            client.publish(topic, messaggio_json)
            
            # Aggiorna il display OLED con i dati del posto corrente
            aggiorna_display(posto["id"], distanza, occupato)
            
        else:
            print(f"Errore lettura sensore per {posto['id']}")
            oled.fill(0)
            oled.text(f"Errore sensore", 0, 0)
            oled.text(f"Posto: {posto['id']}", 0, 20)
            oled.mostra()

        time.sleep(1)  # Pausa tra un sensore e l'altro

    # Pausa prima di ripetere il ciclo per tutti i sensori
    time.sleep(2)