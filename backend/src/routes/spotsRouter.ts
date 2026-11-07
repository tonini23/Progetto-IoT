import { Router } from "express"
import { getSpots, updateSpotReading, updateSpotThreshold } from "../controllers/spotsController"

const router = Router()

router.get("/spots", getSpots)
router.post("/spots/:id/reading", updateSpotReading)
router.patch("/spots/:id/threshold", updateSpotThreshold)

export default router