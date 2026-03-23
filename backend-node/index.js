import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import scanTextRouter from './routes/scanTextRoutes.js';
import scanUrlRouter from './routes/scanUrlRoutes.js';

// 1. App Config
dotenv.config();
const app = express();
const port = process.env.PORT || 5000;

// Middleware so React can talk to Node
app.use(cors());
app.use(express.json());  // This allows Node to read JSON data

// 2. The Router Connection
// This tells Node: "Any request starting with /api/text should look at textRouter"
app.use('/api/text',scanTextRouter);
app.use('/api/url',scanUrlRouter);

// Start the Node server
app.listen(port, () => {
    console.log(`server started at ${port}`);
});