import express from "express";
import { config as configDotenv } from "dotenv";
import { GoogleGenerativeAI } from "@google/generative-ai";
import cors from 'cors';
import https from 'https';
import fs from 'fs';

configDotenv();
const port = process.env.PORT || 3000;
const app = express();

app.use(cors());
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);

// Check if API key is provided
if (!process.env.GEMINI_API_KEY) {
  console.error("Error: GEMINI_API_KEY is missing from environment variables.");
  process.exit(1);
}

// Function to summarize the terms and conditions
async function summarizeTerms(text) {
  try {
    const model = await genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
    const result = await model.generateContent(`Summarize the following terms and conditions in bullet points:\n\n${text}`);
    return result.response.text();
  } catch (error) {
    throw new Error("Error generating summary: " + error.message);
  }
}

// POST route to handle terms and conditions summarization
app.post("/summarize", async (req, res) => {
  console.log("summarizing...")
  const { terms } = req.body;

  // Error handling for missing or invalid request body
  if (!terms || typeof terms !== "string") {
    return res.status(400).json({ error: "Invalid request: 'terms' must be a non-empty string." });
  }

  try {
    const summary = await summarizeTerms(terms);
    res.json({ summary });
  } catch (error) {
    console.error(error.message);
    res.status(500).json({ error: "Failed to generate summary." });
  }
});

// app.listen(port, () => {
//   console.log(`Server running on port ${port}`);
// });

// Load SSL credentials and create an HTTPS server
// const privateKey = fs.readFileSync();
// const certificate = fs.readFileSync();
// const credentials = { key: privateKey, cert: certificate };
// https.createServer(credentials, app).listen(port, () => {
//   console.log(`Server running on port ${port}...`);
// });

export default app;
