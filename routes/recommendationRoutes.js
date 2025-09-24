const express = require("express");
const router = express.Router();

const {
    handleGetRecommendation,
    handleUpdateRecommendation,
    handleDeleteRecommendation,
    handleCreateRecommendation
} = require("../controllers/recommendationController");

router.use(express.json());
router.use(express.urlencoded({ extended: true }));

//Recommendation routes
router.get("/:id", handleGetRecommendation);
router.post("/", handleCreateRecommendation);
router.put("/:id", handleUpdateRecommendation);
router.delete("/:id", handleDeleteRecommendation);

module.exports = router;