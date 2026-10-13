import { Router } from "express"
import { getSpots, updateSpotReading } from "../controllers/spotsController"

const router = Router()

router.get("/spots", getSpots)
router.post("/spots/:id/reading", updateSpotReading)

export default router