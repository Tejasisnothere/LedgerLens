const Item = require("../models/itemModel");
const Inventory = require("../models/inventoryModel");
const Log = require("../models/logModel");


// Get all items
async function handleGetItem(req, res) {
    try {
        const items = await Item.find({}).populate("createdBy", "name email");
        res.json({ success: true, data: items });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Item by id
async function handleGetItemById(req, res) {
    // Incase it is required I'll add later on
}

// Create item
async function handleCreateItem(req, res) {
    try {
        const {
            name,
            amountBuy,
            priceBoughtPerItem,
            priceSoldPerItem,
            createdBy,
            inventoryId,
            fundDeduction
        } = req.body;

        if (!name || !amountBuy || !priceBoughtPerItem || !priceSoldPerItem || !createdBy || !inventoryId) {
            return res.status(400).json({ success: false, error: "Missing required fields" });
        }

        const sameItem = await Item.findById({inventoryId})

        const item = new Item({ name, amountBuy, priceBoughtPerItem, priceSoldPerItem, createdBy });
        await item.save();

        // Update inventory: push new item & deduct funds
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
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}


// Update item
async function handleUpdateItem(req, res) {
    try {
        const { itemId, inventoryId, name, amountBuy, priceBoughtPerItem, priceSoldPerItem } = req.body;

        if (!itemId || !inventoryId)
            return res.status(400).json({ success: false, error: "Missing itemId or inventoryId" });

        const item = await Item.findById(itemId);
        if (!item) return res.status(404).json({ success: false, error: "Item not found" });

        const inventory = await Inventory.findById(inventoryId);
        if (!inventory) return res.status(404).json({ success: false, error: "Inventory not found" });

        const oldAmount = item.amountBuy;

        const oldTotal = item.amountBuy * item.priceBoughtPerItem;
        const newTotal = (amountBuy ?? item.amountBuy) * (priceBoughtPerItem ?? item.priceBoughtPerItem);
        const fundDifference = oldTotal - newTotal;

        if (name) item.name = name;
        if (amountBuy !== undefined) item.amountBuy = amountBuy;
        if (priceBoughtPerItem !== undefined) item.priceBoughtPerItem = priceBoughtPerItem;
        if (priceSoldPerItem !== undefined) item.priceSoldPerItem = priceSoldPerItem;

        await item.save();

        inventory.funds += fundDifference;
        await inventory.save();

        const log = new Log({
            logOf: item._id,
            quantity: amountBuy - oldAmount,
        })
        if(log.quantity !== 0) await log.save();


        res.json({ success: true, data: item, updatedFunds: inventory.funds });
    } catch (err) {
        console.error("Update item error:", err);
        res.status(500).json({ success: false, error: err.message });
    }
}


// Delete Item
const handleDeleteItem = async (req, res) => {
    try {
        const { itemId, inventoryId } = req.body;

        if (!itemId || !inventoryId) {
            return res.status(400).json({ success: false, error: "Missing itemId or inventoryId" });
        }

        const deletedItem = await Item.findByIdAndDelete(itemId);
        if (!deletedItem) {
            return res.status(404).json({ success: false, error: "Item not found" });
        }

        const updatedInventory = await Inventory.findByIdAndUpdate(
            inventoryId,
            { $pull: { ItemList: itemId } },
            { new: true }
        );

        if (!updatedInventory) {
            return res.status(404).json({ success: false, error: "Inventory not found" });
        }

        res.status(200).json({ success: true, message: "Item deleted successfully", inventory: updatedInventory });
    } catch (error) {
        console.error("Delete item error:", error);
        res.status(500).json({ success: false, error: "Server error" });
    }
};

// Get all inventories
async function handleGetInventory(req, res) {
    try {
        const inventories = await Inventory.find({}).populate("ItemList");
        res.json({ success: true, data: inventories });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Create inventory
async function handleCreateInventory(req, res) {
    try {
        const { name, funds, createdBy } = req.body;

        if (!name || funds === undefined || !createdBy) {
            return res.status(400).json({ success: false, error: "Missing fields" });
        }

        const inventory = new Inventory({
            name,
            funds,
            createdBy,
            ItemList: []
        });

        await inventory.save();

        res.status(201).json({ success: true, data: inventory });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Update inventory
async function handleUpdateInventory(req, res) {
    try {
        const { id, name, funds } = req.body;
        const inventory = await Inventory.findById(id);
        if (!inventory) return res.status(404).json({ success: false, error: "Inventory not found" });

        if (name) inventory.name = name;
        if (funds !== undefined) inventory.funds = funds;

        await inventory.save();

        res.json({ success: true, data: inventory });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

// Delete inventory
async function handleDeleteInventory(req, res) {
    try {
        const id  = req.body.id;
        const inventory = await Inventory.findByIdAndDelete(id);
        if (!inventory) return res.status(404).json({ success: false, error: "Inventory not found" });

        res.json({ success: true, message: "Inventory deleted successfully" });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

//Get Inventory by ID
async function handleGetInventoryById(req, res) {
    try {
        const { id } = req.params;
        const inventory = await Inventory.findById(id).populate("ItemList");
        if (!inventory) {
            return res.status(404).json({ success: false, error: "Inventory not found" });
        }
        res.json({ success: true, data: inventory });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
}

module.exports = {
    handleGetItem,
    handleCreateItem,
    handleUpdateItem,
    handleDeleteItem,
    handleGetItemById,
    handleGetInventory,
    handleCreateInventory,
    handleUpdateInventory,
    handleDeleteInventory,
    handleGetInventoryById
};
