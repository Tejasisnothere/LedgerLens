const {Schema, model} = require("mongoose");

const logSchema = new Schema({
    logOfInv: {
        type: Schema.Types.ObjectId,
        ref: "Inventory",
        required: true
    },
    logOfItm: {
        type: Schema.Types.ObjectId,
        ref: "Item",
        required: true
    },
    name: {
        type: String,
        required: true
    },
    profit: {
        type: Number,
        required: true
    },
    quantity: {
        type: Number,
        required: true
    },
    category: {
        type: String,
        required: true
    }
}, {timestamps: true});

const Log = model("log", logSchema);

module.exports = Log;