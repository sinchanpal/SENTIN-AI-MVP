import express from "express"
import { scanUrl } from "../controllers/scanUrlController.js";

const scanUrlRouter = express.Router();

// When a POST request hits /scan-text, send it to the scanText controller function!
scanUrlRouter.post('/scan-url', scanUrl);

export default scanUrlRouter;