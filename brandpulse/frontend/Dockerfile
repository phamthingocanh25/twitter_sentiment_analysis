# STAGE 1: Build ứng dụng React
FROM node:18-alpine AS build

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép package.json và package-lock.json
COPY package*.json ./

# Cài đặt các dependencies
RUN npm install

# Sao chép toàn bộ source code
COPY . .

# Build ứng dụng cho production
RUN npm run build

# STAGE 2: Serve ứng dụng bằng Nginx
FROM nginx:1.21-alpine

# Sao chép kết quả build từ stage 1 vào thư mục public của Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Sao chép file cấu hình Nginx (nếu có, không bắt buộc cho app đơn giản)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Mở cổng 80
EXPOSE 80

# Lệnh để khởi động Nginx
CMD ["nginx", "-g", "daemon off;"]
