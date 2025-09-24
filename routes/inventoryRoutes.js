const router = require("express").Router();
const {
    handleGetInventory,
    handleCreateInventory,
    handleUpdateInventory,
    handleDeleteInventory,
    handleGetItem,
    handleCreateItem,
    handleUpdateItem,
    handleDeleteItem, handleGetItemById, handleGetInventoryById
} = require("../controllers/inventoryController");

// Item routes
router.get("/getItem", handleGetItem);
router.post("/createItem", handleCreateItem);
router.patch("/updateItem", handleUpdateItem);
router.delete("/deleteItem", handleDeleteItem);
router.get("/getItemById:id", handleGetItemById);

// Inventory routes
router.get("/getInventory", handleGetInventory);
router.post("/createInventory", handleCreateInventory);
router.post("/updateInventory", handleUpdateInventory);
router.delete("/deleteInventory", handleDeleteInventory);
router.get("/getInventoryById/:id", handleGetInventoryById);

module.exports = router;
