import express, { Express } from "express"
//import autoriRouter from "./routes/autori-router"
import historyApiFallback from "connect-history-api-fallback"

const app: Express = express()
const port: number = 3000

app.use(historyApiFallback())

app.use(express.static("dist-frontend"))
app.use(express.static("public"))

//app.use(articoliRouter)

app.use(function(req, res, next) {
  res.setHeader("Content-Type", "text/plain")
  res.status(404).send("Ops... Pagina non trovata")
})

app.listen(port, function() {
  console.log(`Listening on http://localhost:${port}`)
})
