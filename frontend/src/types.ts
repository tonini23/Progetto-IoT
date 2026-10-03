// Un posto auto, come descritto in public/spots.json
export interface Spot {
  id: string          // es. "A-101"
  row: string         // "A" (fila sopra) oppure "B" (fila sotto)
  disabled: boolean   // true = posto per disabili
}

// Ultimo stato ricevuto via MQTT per un posto
export interface SpotState {
  occupied: boolean
  distance: number | null   // distanza in cm letta dal sensore (se disponibile)
  time: number              // quando e' arrivato il messaggio (ms)
}