const Event = require("../models/eventModel");

const handleCreateEvent = async (req, res) => {
    try {
        const { name, type, startDate, endDate, eventOf } = req.body;

        if(!name || !type || !startDate || !endDate) {
            return res.status(400).send({message: "Missing credentials"});
        }

        const event = new Event({
            name,
            type,
            startDate,
            endDate,
            eventOf
        })
        await event.save();
        return res.status(200).json({ success: true, event });

    }catch(err){
        return res.status(500).send({ success: false, error: err});
    }
};

const handleUpdateEvent = async (req, res) => {
    // Update said event, not really a lot of scope here but let's keep it here
};

const handleDeleteEvent = async (req, res) => {
    try{

    }catch(err){
        return res.status(500).send({success: false, error: err});
    }
};

const handleGetEvent = async (req, res) => {
    // Handle getting events for a given inventory/shop
};

module.exports = {
    handleCreateEvent,
    handleUpdateEvent,
    handleGetEvent,
    handleDeleteEvent,
}