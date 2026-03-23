import axios from "axios";


export const scanText = async (req, res) => {
    try {
        // 1. The Waiter (React) hands us the order
        const { userText } = req.body;
        // console.log("Received text from the user : ", userText);

        const pythonServerURL= process.env.PYTHON_SERVER_URL;
        // 2. The Manager (Node) walks over to the Chef (Python)
        const pythonResponse = await axios.post(`${pythonServerURL}/api/analyze-text`, {
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
}