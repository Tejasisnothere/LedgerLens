const express = require("express");
const connectDB = require("./db");

const userRoutes = require("./routes/userRoutes");
const inventoryRoutes = require("./routes/inventoryRoutes");
const itemRoutes = require("./routes/itemRoutes");
const eventRoutes = require("./routes/eventRoutes");
const recommendationRoutes = require("./routes/recommendationRoutes");
const logRoutes = require("./routes/logRoutes");

require("dotenv").config();

const app = express();
const cors = require("cors");
const PORT = process.env.PORT || 8080;

connectDB();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors());

app.use("/api/users", userRoutes);
app.use("/api/inventories", inventoryRoutes);
app.use("/api/recommendations", recommendationRoutes);
app.use("/api/items", itemRoutes);
app.use("/api/events", eventRoutes);
app.use("/api/logs", logRoutes);

//Once hosted on AWS (ECS or BeanStalk) just check this thing on postman using the provided environment link from AWS; use this in POSTMAN
app.get("/", (req, res) => {
    res.status(200).send({message: "Hello from the server pookie"});
})

app.listen(PORT,  () => {
    console.log(`Server started on port ${PORT}`);
});
