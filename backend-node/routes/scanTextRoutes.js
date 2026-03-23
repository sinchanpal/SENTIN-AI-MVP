import express from "express"
import { scanText } from "../controllers/scanTextController.js";

const scanTextRouter = express.Router();

// When a POST request hits /scan-text, send it to the scanText controller function!
scanTextRouter.post('/scan-text', scanText);

export default scanTextRouter;