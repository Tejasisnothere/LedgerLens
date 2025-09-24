const { Schema, model } = require("mongoose");
const jwt = require("jsonwebtoken");
const { createHmac, randomBytes } = require("crypto");

const userSchema = new Schema({
    name: {
        type: String,
        required: true,
        unique: false
    },
    email: {
        type: String,
        required: true,
        unique: true
    },
    salt: {
        type: String,
    },
    password: {
        type: String,
        required: true,
    },
    subscription: {
        type: Number,
        default: 0
    }
}, { timestamps: true });

userSchema.pre("save", function (next) {
    const user = this;

    if (!user.isModified("password")) return next();

    const salt = randomBytes(16).toString("hex");
    const hashedPassword = createHmac("sha256", salt).update(user.password).digest("hex");

    user.salt = salt;
    user.password = hashedPassword;

    next();
});

const createTokenForUser = (user) => {
    return jwt.sign(
        { id: user._id, email: user.email },
        process.env.JWT_SECRET || "supersecretkey",
        { expiresIn: "7d" }
    );
};

userSchema.statics.matchPasswordAndGenerateToken = async function (email, password) {
    const user = await this.findOne({ email });
    if (!user) throw new Error("User not found");

    const userProvidedHash = createHmac("sha256", user.salt)
        .update(password)
        .digest("hex");

    if (user.password === userProvidedHash) {
        const token = createTokenForUser(user);
        return { user, token };
    }

    throw new Error("Invalid credentials");
};

const User = model("User", userSchema);

module.exports = User;
