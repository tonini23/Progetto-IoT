import mqtt from 'mqtt';
import { connection } from './db';

const MQTT_BROKER = 'mqtt://broker.emqx.io:1883';
const MQTT_TOPIC = 'parking/spots/+';
// '+' -> wildcard per tutti i posti auto, es. parking/spots/A-101 ... A-102 ecc.


export function startMqttBroker() {
  const mqttClient = mqtt.connect(MQTT_BROKER);

  mqttClient.on('connect', () => {
    console.log(' Connesso al Broker MQTT ');
    mqttClient.subscribe(MQTT_TOPIC, (err) => {
      if (err) console.error('Errore iscrizione topic:', err);
    });
  });

  mqttClient.on('message', async (topic, message) => {
    try {
      const dati = JSON.parse(message.toString());
      const spot_id = topic.split('/').pop();
      
      // Traduce il booleano "occupato" di Python in 'BUSY' o 'FREE' per il DB
      const new_status = dati.occupato ? 'BUSY' : 'FREE';
      const distance = dati.distanza_cm ?? null; // Legge la distanza se presente

      await connection.promise().execute(
        'UPDATE parking_spots SET status = ?, current_distance = ? WHERE id = ?',
        [new_status, distance, spot_id]
      );
      

      console.log(`Aggiornato ${spot_id} a ${new_status}`);
    } catch (error) {
      console.error('Errore durante la gestione del messaggio MQTT:', error);
    }
  });
}