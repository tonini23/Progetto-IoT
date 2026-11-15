import express, { Express } from "express"
import historyApiFallback from "connect-history-api-fallback"
import spotsRouter from "./routes/spotsRouter"
import { startMqttBroker } from "./utils/broker"

const app: Express = express()
const port: number = 3000

// Permette alle API REST di leggere i body JSON delle richieste.
app.use(express.json())

// Le API devono essere registrate prima del fallback della Single Page Application.
app.use("/api", spotsRouter)

// Fallback per le rotte gestite da Vue Router.
app.use(historyApiFallback())

// File statici del frontend compilato e file pubblici.
app.use(express.static("dist-frontend"))
app.use(express.static("public"))

app.use(function (req, res) {
  res.setHeader("Content-Type", "text/plain")
  res.status(404).send("Ops... Pagina non trovata")
})

// Avvia un solo client MQTT: la gestione dei messaggi è in utils/broker.ts.
startMqttBroker()

app.listen(port, function () {
  console.log(`Listening on http://localhost:${port}`)
})
