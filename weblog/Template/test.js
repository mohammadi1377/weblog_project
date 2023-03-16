const jwt = require('jsonwebtoken');

// Generate a JWT for the user
const user = { id: 123, username: 'johndoe' };
const token = jwt.sign(user, 'your_secret_key');

// Verify the JWT
const decoded = jwt.verify(token, 'your_secret_key');

// Include the JWT in API requests
fetch('/api/data', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
