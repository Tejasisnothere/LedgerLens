const express = require("express");

const {handleLoginUser, handleDeleteUser, handleCreateUser, handleUpdateUser} = require("../controllers/userController")

const router = express.Router();

router.post("/login", handleLoginUser);
router.post("/signup", handleCreateUser);
router.patch("/updateUser", handleUpdateUser);
router.post("/deleteUser", handleDeleteUser);

module.exports = router;