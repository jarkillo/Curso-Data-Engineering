# Frontend Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Copy application
COPY . .

# Expose port
EXPOSE 5173

# Install dependencies and run development server
CMD npm install && npm run dev -- --host 0.0.0.0
