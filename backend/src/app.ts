import express, { Express } from "express"
import spotsRouter from "./routes/spotsRouter"
import historyApiFallback from "connect-history-api-fallback"
import mqtt from "mqtt"
import { connection } from "./utils/db" 

const app: Express = express()
const port: number = 3000

app.use(historyApiFallback())

app.use(express.static("dist-frontend"))
app.use(express.static("public"))

app.use("/api", spotsRouter)
app.use(function(req, res, next) {
  res.setHeader("Content-Type", "text/plain")
  res.status(404).send("Ops... Pagina non trovata")
})


// CONFIGURAZIONE MQTT CON SCRITTURA SU DB

const MQTT_BROKER = "mqtt://broker.emqx.io"
const MQTT_TOPIC = "parking/spots/#"

const mqttClient = mqtt.connect(MQTT_BROKER)

mqttClient.on("connect", () => {
  console.log("Connesso al broker MQTT con successo!")
  mqttClient.subscribe(MQTT_TOPIC, (err) => {
    if (!err) {
      console.log(`Iscritto al topic: ${MQTT_TOPIC}`)
    }
  })
})

mqttClient.on("message", async (topic, message) => {
  try {
    const payload = JSON.parse(message.toString())
    // Payload atteso dall'ESP32
    const spotId = payload.id
    const distance = payload.distanza_cm

    if (spotId !== undefined && distance !== undefined) {
      // 1. Recupera la soglia dal database per calcolare lo stato (BUSY/FREE)
      const [spots]: any = await connection.promise().query(
        "SELECT threshold_cm FROM parking_spots WHERE id = ?",
        [spotId]
      )

      if (spots.length > 0) {
        const threshold = spots[0].threshold_cm ?? 50
        const newStatus = distance < threshold ? "BUSY" : "FREE"
        const now = new Date()

        // 2. Aggiorna il database con la distanza, lo stato e il timestamp dell'ultimo aggiornamento
        await connection.promise().query(
          "UPDATE parking_spots SET status = ?, current_distance = ?, last_update = ? WHERE id = ?",
          [newStatus, distance, now, spotId]
        )

        console.log(`Posto ${spotId} aggiornato nel DB -> Distanza: ${distance}cm, Stato: ${newStatus}`);
      }
    }
  } catch (error) {
    console.error("Errore nell'elaborazione del messaggio MQTT su DB:", error)
  }
})


app.listen(port, function() {
  console.log(`Listening on http://localhost:${port}`)
})