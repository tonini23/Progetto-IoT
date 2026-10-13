import { Request, Response } from "express"
import { connection } from "../utils/db"

export const getSpots = async (req: Request, res: Response): Promise<void> => {
  try {
    const [rows]: any = await connection.promise().query("SELECT * FROM parking_spots")

    const formattedSpots = rows.map((spot: any) => {

      const rawId = spot.id 
      
      // Estrae la lettera della fila (es. "A" da "A-101") in modo sicuro
      const row = typeof rawId === "string" && rawId.includes("-") 
        ? rawId.split("-")[0] 
        : "A"

      const isOccupied = spot.status === "BUSY"

      return {
        id: String(rawId),
        row: row,
        disabled: spot.spot_type === "disabled",
        occupied: spot.status ? isOccupied : null,
        distance: spot.current_distance ?? null,
        time: spot.last_update ? new Date(spot.last_update).getTime() : Date.now()
      }
    })

    res.json(formattedSpots)
  } catch (error) {
    console.error("Errore recupero spots:", error)
    res.status(500).json({ error: "Errore interno del server" })
  }
}

export const updateSpotReading = async (req: Request, res: Response): Promise<void> => {
  try {
    const { id } = req.params
    const { distance } = req.body

    // Soglia in cm (se la distanza è minore di 50 cm il posto è occupato)
    const threshold = 50
    const newStatus = distance < threshold ? "BUSY" : "FREE"

    await connection.promise().query(
      "UPDATE parking_spots SET status = ?, current_distance = ? WHERE id = ?",
      [newStatus, distance, id]
    )

    res.json({
      success: true,
      id,
      status: newStatus,
      distance
    })
  } catch (error) {
    console.error("Errore aggiornamento lettura:", error)
    res.status(500).json({ error: "Errore interno del server" })
  }
}