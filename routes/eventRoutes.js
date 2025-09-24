const express = require("express");
const router = express.Router();

const {
    handleGetEvent,
    handleCreateEvent,
    handleDeleteEvent,
    handleUpdateEvent
} = require("../controllers/eventController")

router.use(express.json());
router.use(express.urlencoded({ extended: true }));

//Event routes
router.get("/:id", handleGetEvent);
router.put("/:id", handleUpdateEvent);
router.delete("/:id", handleDeleteEvent);
router.post("/", handleCreateEvent);

module.exports = router;