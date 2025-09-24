const Log = require("../models/logModel");
const { Schema, model } = require("mongoose");

const analysisSchema = new Schema({
    description: {
        type: String,
        required: true
    },
    createdBy: {
        type: Schema.Types.ObjectId,
        ref: "User",
        required: true
    }
}, { timestamps: true });

const Analysis = model("Analysis", analysisSchema);

const handleGetAnalysis = async (req, res) => {
    try {
        const analysis = await Analysis.find().populate("createdBy", "name email");
        res.status(200).json({ success: true, data: analysis });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

const handleCreateAnalysis = async (req, res) => {
    try {
        const { description, createdBy } = req.body;
        if (!description || !createdBy) {
            return res.status(400).json({ success: false, error: "Description and createdBy are required" });
        }

        const newAnalysis = new Analysis({ description, createdBy });
        await newAnalysis.save();

        res.status(201).json({ success: true, data: newAnalysis });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

const handleDeleteAnalysis = async (req, res) => {
    try {
        const { id } = req.params;
        await Analysis.findByIdAndDelete(id);
        res.status(200).json({ success: true, message: "Analysis deleted" });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

const handleGetLogs = async (req, res) => {
    try {
        const logs = await Log.find().populate("logOf", "name amount pricePerItem");
        res.status(200).json({ success: true, data: logs });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

const handleCreateLogs = async (req, res) => {
    try {
        const { logOf, quantity } = req.body;
        if (!logOf || !quantity) {
            return res.status(400).json({ success: false, error: "logOf and quantity are required" });
        }

        const newLog = new Log({ logOf, quantity });
        await newLog.save();

        res.status(201).json({ success: true, data: newLog });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

const handleDeleteLogs = async (req, res) => {
    try {
        const { id } = req.params;
        await Log.findByIdAndDelete(id);
        res.status(200).json({ success: true, message: "Log deleted" });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

const handleGetTimedLogs = async (req, res) => {
    try{
        const {inventoryId, itemId} = req.body;
        if(!inventoryId || !itemId){
            return res.send({success: false, error: "Missing credentials"});
        }
        const timedLogs = await Log.aggregate([
            { $group: {
                    id: inventoryId,
                }
            }
        ])
    }catch(err){
        return res.status(500).send({success: false, error: err});
    }
};

const handleGetItemLogs = async (req, res) => {
    //In case we require itemised logs
};

module.exports = {
    handleGetAnalysis,
    handleCreateAnalysis,
    handleDeleteAnalysis,

    handleGetLogs,
    handleCreateLogs,
    handleDeleteLogs
};
