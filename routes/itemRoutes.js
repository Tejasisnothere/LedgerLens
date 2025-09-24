const express = require("express");
const router = express.Router();

const {
    handleGetItemById,
    handleCreateItem,
    handleDeleteItem,
    handleUpdateItem
} = require("../controllers/itemController");

router.use(express.json());
router.use(express.urlencoded({ extended: true }));

//Item routes
router.get("/:id", handleGetItemById);
router.put("/:id", handleUpdateItem);
router.delete("/", handleDeleteItem);
router.post("/", handleCreateItem);

module.exports = router;