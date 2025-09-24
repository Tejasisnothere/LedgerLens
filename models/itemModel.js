const {Schema, model} = require("mongoose");

const itemSchema = new Schema({
    name: {
        type: String,
        required: true
    },
    amountBuy: {
        type: Number,
        required: true,
        default: 0
    },
    priceBoughtPerItem: {
        type: Number,
        required: true,
        default: 0
    },
    priceSoldPerItem: {
        type: Number,
        required: true
    },
    createdBy: {
        type: Schema.Types.ObjectId,
        ref: "Inventory",
        required: true
    }
}, {timestamps: true});

const Item = model("Item", itemSchema);

module.exports = Item;