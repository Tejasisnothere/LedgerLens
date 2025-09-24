const Item = require("../models/itemModel");
const Inventory = require("../models/inventoryModel");
const Log = require("../models/logModel");

const handleCreateItem = async (req, res) => {
    try{
        const {
            name,
            amountBuy,
            category,
            priceBoughtPerItem,
            priceSoldPerItem,
            createdBy,
            inventoryId,
            fundsDeduction
        } = req.body;

        if(!name || !amountBuy || !category || !priceBoughtPerItem || !priceSoldPerItem || !createdBy || !inventoryId || !fundsDeduction) {
            return res.status(400).json({ success: false, message: "Missing credentials" });
        }

        const item = new Item({
            name,
            amountBuy,
            category,
            priceBoughtPerItem,
            priceSoldPerItem,
            createdBy,
        });
        await item.save();

        const inventory = await Inventory.findById(inventoryId);
        if (!inventory) return res.status(404).json({ success: false, error: "Inventory not found" });

        inventory.ItemList.push(item._id);

        if (fundDeduction && !isNaN(fundDeduction)) {
            inventory.funds -= Number(fundDeduction);
        }

        await inventory.save();

        const log = new Log({
            logOf: item._id,
            quantity: amountBuy
        });
        await log.save();

        res.status(201).json({ success: true, data: item, updatedFunds: inventory.funds });

    }catch(err){
        return res.status(500).send({success: false, error: err});
    }
};

const handleUpdateItem = async (req, res) => {
    try{
        const { itemId, inventoryId, name, amountBuy, category, priceBoughtPerItem, priceSoldPerItem } = req.body;

        const item = await Item.findById(itemId);
        if(!item){
            return res.status(404).send({error: "Item not found"});
        }

        const inventory = await Inventory.findById(inventoryId);
        if(!inventory){
            return res.status(404).send({error: "Inventory not found"});
        }

        const oldAmount = Number(item.amountBuy);

        const oldTotal = item.amountBuy * item.priceBoughtPerItem;
        const newTotal = (amountBuy ?? item.amountBuy) * (priceBoughtPerItem ?? item.priceBoughtPerItem);
        const fundsDifference = oldTotal - newTotal;

        if(name) item.name = name;
        if(amountBuy !== undefined) item.amountBuy = amountBuy;
        if(priceBoughtPerItem !== undefined) item.priceBoughtPerItem = priceBoughtPerItem;
        if(priceSoldPerItem !== undefined) item.priceSoldPerItem = priceSoldPerItem;
        await item.save();

        inventory.funds -= fundsDifference;
        await inventory.save();

        const log = new Log({
            logOfIvn, logOfItm, name, amountBuy, priceSoldPerItem, priceBoughtPerItem
        })

    }catch(err){
        return res.status(500).send({ success: false, error: err })
    }
};

const handleDeleteItem = async (req, res) => {
    try{
        const { itemId, inventoryId } = req.body;
        const item = await Item.findByIdAndDelete(itemId);
        if(!item){
            return res.status(404).send({error: "Item not found"});
        }

        const inventory = await Inventory.findById(
            inventoryId,
            { $pull: { ItemList: itemId } },
            { new: true }
        );

        if(!inventory){
            return res.status(404).send({error: "Inventory not found"});
        }

        return res.status(200).json({success: true, inventory: inventory});
    }catch(err){
        return res.status(500).send({success: false, error: err});
    }
};

const handleGetItemById = async (req, res) => {
    try {
        const items = await Item.find({}).populate("createdBy", "name email");
        res.json({ success: true, data: items });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};

const getPopularItem = async (req, res) => {
    try {
        const { type = "quantity", limit = 1 } = req.body;

        const sortField = type === "profit" ? "profit" : "quantity";

        const items = await Log.aggregate([
            {
                $group: {
                    _id: "$logOfItm",
                    name: { $first: "$name" },
                    category: { $first: "$category" },
                    totalQuantity: { $sum: "$quantity" },
                    totalProfit: { $sum: "$profit" }
                }
            },
            {
                $sort: sortField === "profit"
                    ? { totalProfit: -1 }
                    : { totalQuantity: -1 }
            },
            { $limit: limit }
        ]);

        return res.status(200).send({ success: true, data: items });
    } catch (err) {
        return res.status(500).send({ success: false, error: err.message });
    }
};

const getRunningLow = async (req, res) => {
    try{
        const {

        } = req.body;
    }catch(err){
        return res.status(500).send({success: false, error: err});
    }
}

const getUnpopularItem = async (req, res) => {
    try{
        const {

        } = req.body;
    }catch(err){
        return res.status(500).send({success: false, error: err});
    }
};

module.exports = {
    handleGetItemById,
    handleUpdateItem,
    handleDeleteItem,
    handleCreateItem,
    getPopularItem,
    getUnpopularItem,
    getRunningLow
}