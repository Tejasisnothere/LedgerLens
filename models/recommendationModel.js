const {model, Schema} = require("mongoose");

const recommendationSchema = new Schema({
    recOf: {
        type: Schema.Types.ObjectId,
        ref: 'Item',
    },
    recIn: {
        type: Schema.Types.ObjectId,
        ref: "Inventory"
    },
    text: { // A shortened version of the text return from gemini API so that we have some sort of log of what the recommendation was about
        type: String,
    },
    category: { //This will store "inc" or "dec" indicating the type of the recommendation in case there is a call
        type: String,
    }
}, {timestamps: true});

const Recommendation = model("Recommendation", recommendationSchema);

module.exports = Recommendation;