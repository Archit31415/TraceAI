function authenticateUser(userPayload) {
    console.log("Authenticating...");
    
    const sessionToken = userPayload.credentials.token;
    
    return sessionToken;
}

authenticateUser(null);