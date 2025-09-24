const Recommendation = require("../models/recommendationModel");

const handleCreateRecommendation = async (req, res) => {
    // Creating a new recommendation based on events or other stuff
};

const handleDeleteRecommendation = async (req, res) => {
    // Delete these after a certain period of time
};

const handleGetRecommendation = async (req, res) => {
    // Will get all the recommendations for the particular inventory/shop
};

const handleUpdateRecommendation = async (req, res) => {
    // So for this it'll update the recommendation, but let's keep it in the pipeline in case we use it
};

module.exports = {
    handleCreateRecommendation,
    handleDeleteRecommendation,
    handleUpdateRecommendation,
    handleGetRecommendation
}