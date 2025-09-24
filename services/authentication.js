const JWT = require('jsonwebtoken');

const secret = process.env.JWT_SECRET || "HEHEHUHU";

function createTokenForUser(user) {
    const payload = {
        _id: user._id,
        email: user.email,
        profileImageUrl: user.profileImageUrl,
        role: user.role,
        name: user.name,
        username: user.username
    };
    const token = JWT.sign(payload, secret);
    return token
}

function validateToken(token) {
    const payload = JWT.verify(token, secret);
    return payload;
}

module.exports = {
    createTokenForUser,
    validateToken
}