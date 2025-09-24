import express from "express";

const router = express.Router();

// Logs
router.get("/getLogs", handleGetLogs);
router.post("/createLogs", handleCreateLogs);
router.post("/deleteLogs", handleDeleteLogs);

// Analysis
router.get("/getAnalysis", handleGetAnalysis);
router.post("/createAnalysis", handleCreateAnalysis);
router.post("/deleteAnalysis", handleDeleteAnalysis);

module.exports = router;