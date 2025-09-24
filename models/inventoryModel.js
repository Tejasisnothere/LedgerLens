const { Schema, model, Types } = require("mongoose");

const inventorySchema = new Schema({
    name: { type: String, required: true },
    createdBy: { type: Schema.Types.ObjectId, ref: "User", required: true },
    ItemList: [{ type: Schema.Types.ObjectId, ref: "Item" }],
    funds: { type: Number, required: true }
});

module.exports = model("Inventory", inventorySchema);
