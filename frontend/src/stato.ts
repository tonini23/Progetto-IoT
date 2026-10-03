// Stato condiviso da tutte le pagine
// I dati arrivano dal backend  (API /api/spots), che li legge dal database
import { ref, reactive } from "vue"
import axios from "axios"
import type { Spot, SpotState } from "./types"

// Come risponde il backend per ogni posto
interface PostoApi {
  id: string
  row: string
  disabled: boolean
  occupied: boolean | null   // null = nessuna lettura ancora arrivata
  distance: number | null
  time: number | null
}

export const spots = ref<Spot[]>([])                          // elenco dei posti
export const states = reactive<Record<string, SpotState>>({}) // id posto -> ultimo stato

let started = false

// "free", "busy" oppure "unknown" (se non c'e' ancora nessuna lettura)
export function statusOf(id: string): string {
  const s = states[id]
  if (!s) return "unknown"
  return s.occupied ? "busy" : "free"
}

// chiede i dati al backend e aggiorna le variabili
async function aggiorna() {
  try {
    const res = await axios.get<PostoApi[]>("/api/spots")

    spots.value = res.data.map(p => ({ id: p.id, row: p.row, disabled: p.disabled }))

    for (const p of res.data) {
      if (p.occupied === null) {
        delete states[p.id]
      } else {
        states[p.id] = {
          occupied: p.occupied,
          distance: p.distance,
          time: p.time ?? Date.now()
        }
      }
    }
  } catch (err) {
    console.error("Backend non raggiungibile", err)
  }
}

export function start() {
  if (started) return   // parte una sola volta anche se cambio pagina
  started = true

  aggiorna()
  setInterval(aggiorna, 2000)   // ogni 2 secondi richiedo i dati aggiornati
}