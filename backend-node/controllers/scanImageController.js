import axios from "axios";
import FormData from "form-data";

export const scanImage = async (req, res) => {
    try {
        // 1. The Waiter (React) hands us the heavy box (the image file)
        const file = req.file; 
        
        if (!file) {
            return res.status(400).json({ error: "No image file provided!" });
        }

        // 2. The Manager (Node) repacks the box for the Chef (Python)
        // We have to use FormData because we are sending a file, not simple JSON text.
        const formData = new FormData();
        
        // We attach the file's raw memory data (buffer) and its original name
        formData.append('file', file.buffer, file.originalname);

        const pythonServerURL = process.env.PYTHON_SERVER_URL;

        // 3. The Manager walks over to the Chef
        // Notice we have to tell Axios to use special "headers" so Python knows a file is coming!
        const pythonResponse = await axios.post(`${pythonServerURL}/api/scan-screenshot`, formData, {
            headers: {
                ...formData.getHeaders(),
            }
        });

        // 4. The Chef gives back the ML result, Manager hands it to the Waiter
        const pythonData = pythonResponse.data;
        return res.status(200).json(pythonData);

    } catch (error) {
        console.error("Error talking to Python:", error.message);
        res.status(500).json({ error: "The Python AI server is down or rejected the image!" });
    }
}