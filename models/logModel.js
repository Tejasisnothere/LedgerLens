const {Schema, model} = require("mongoose");

const logSchema = new Schema({
    logOf: {
        type: Schema.Types.ObjectId,
        ref: "Item",
        required: true
    },
    quantity: {
        type: Number,
        required: true
    },
}, {timestamps: true});

const Log = model("log", logSchema);

module.exports = Log;