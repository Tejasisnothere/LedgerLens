const {Schema, model} = require('mongoose');

const analysisSchema = new Schema({
    description: {
        type: String,
    },
})