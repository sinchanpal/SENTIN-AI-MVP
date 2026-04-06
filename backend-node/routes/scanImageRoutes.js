import express from "express";
import multer from "multer";
import { scanImage } from "../controllers/scanImageController.js";



const scanImageRouter = express.Router();

// 1. Tell the security guard (multer) to hold the file in temporary RAM memory
const upload = multer({ storage: multer.memoryStorage() });

// 2. Set up the route. 
// upload.single('screenshot') tells multer: "Look out for a single file attached with the name 'screenshot'"
scanImageRouter.post('/scan-screenshot', upload.single('screenshot'), scanImage);

export default scanImageRouter;