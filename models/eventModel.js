const {model, Schema} = require("mongoose");

const eventSchema = new Schema({
    name: {
        type: String,
        required: true,
    },
    type: {
        type: String,
        required: true
    },
    startDate: {
        type: Date,
        required: true
    },
    endDate: {
        type: Date,
        required: true
    },
    eventOf: {
        type: Schema.Types.ObjectId,
        ref: "Inventory"
    }
}, {timestamps: true});

const Event = model("Event", eventSchema);

module.exports = Event;