# Frontend Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies (cache bust: v2 - added @tailwindcss/typography)
COPY package*.json ./
RUN npm install

# Copy application
COPY . .

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
