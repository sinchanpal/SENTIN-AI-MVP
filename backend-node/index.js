import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'

import axios from 'axios';

// 1. App Config
dotenv.config();
const app = express();
const port = process.env.PORT || 5000;

// Middleware so React can talk to Node
app.use(cors());
app.use(express.json());  // This allows Node to read JSON data

app.post('/api/scan-text', async (req, res) => {

    try {
        // 1. The Waiter (React) hands us the order
        const { userText } = req.body;
        console.log("Receaved text from the user : ", userText);

        // 2. The Manager (Node) walks over to the Chef (Python)
        const pythonResponse = await axios.post('http://127.0.0.1:8000/analyze-text', {
            text: userText
        });

        // 3. The Chef (Python) gives us the ML result
        const pythonData = pythonResponse.data;

        // 4. The Manager (Node) hands the result back to the Waiter (React)

        return res.status(200).json(pythonData);


    } catch (error) {
        console.error("Error talking to Python:", error);
        res.status(500).json({ error: "The Python AI server is down!" });
    }
})

// Start the Node server
app.listen(port, () => {
    console.log(`server started at ${port}`);
});