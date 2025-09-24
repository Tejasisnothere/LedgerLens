const User = require("../models/userModel");

const handleCreateUser = async (req, res) => {
    try {
        const { name, email, password, location } = req.body;
        if (!name || !email || !password) {
            return res.status(400).send({message: "Missing credentials"});
        }

        const existingUser = await User.findOne({email});
        if(existingUser) {
            return res.status(400).send({message: "User already exists"});
        }

        const user = new User({ name, email, password, location });
        await user.save();

        return res.status(201).json({
            message: "User created successfully",
            user: {
                id: user._id,
                name: user.name,
                email: user.email,
                location: user.location
            }
        });
    }catch(err) {
        return res.status(500).send({error: err.message});
    }
}

const handleLogoutUser = async (req, res) => {
    // In case of a website
}

const handleUpdateUser = async (req, res) => {
    try {
        const { id, name, email } = req.body;
        if (!name || !email) {
            return res.status(400).send({ message: "Missing credentials" });
        }

        const user = await User.findById(id);
        if (!user) {
            return res.status(404).send({ message: "User not found" });
        }

        user.name = name;
        user.email = email;

        await user.save();
        return res.send({ success: true, message: "User updated successfully" });
    } catch (err) {
        return res.status(500).send({ error: err.message });
    }
};

const handleDeleteUser = async (req, res) => {
    try{
        const { id } = req.body;
        if(!id){
            return res.status(400).send({message: "What the actual.....?"});
        }
        const user = await User.findByIdAndDelete(id);
        if(!user){
            return res.status(400).send({message: "User not found"});
        }
        return res.json({message: "User deleted successfully"});
    }catch(err){
        return res.status(500).send({error: err.message});
    }
}

const handleLoginUser = async (req, res) => {
    try {
        const { email, password } = req.body;
        if (!email || !password) {
            return res.status(400).json({ message: "Missing credentials" });
        }

        const { user, token } = await User.matchPasswordAndGenerateToken(email, password);
        return res.json({
            message: "Login successful",
            token,
            user: {
                id: user._id,
                name: user.name,
                email: user.email,
                subscription: user.subscription,
            },
        });
    } catch (err) {
        return res.status(400).json({ message: err.message });
    }
}

module.exports = {
    handleUpdateUser,
    handleLoginUser,
    handleCreateUser,
    handleDeleteUser,
    handleLogoutUser
}