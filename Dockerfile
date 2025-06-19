# Use an official Nginx image
FROM nginx:alpine

# Remove default Nginx static assets
RUN rm -rf /usr/share/nginx/html/*

# Copy build output to Nginx's web directory
COPY dist/ /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
