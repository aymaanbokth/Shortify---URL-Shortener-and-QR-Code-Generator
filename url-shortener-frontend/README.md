# 🚀 Shortify - URL Shortener & QR Code Generator  

## 🌟 Overview  
Shortify is a **full-stack URL shortener and QR code generator** built using **Flask (backend) and React (frontend)**. It allows users to shorten long URLs, generate **custom short codes**, track **click analytics**, and create **QR codes** for easy sharing.  

---

## ✨ Features  
✅ **Shorten Long URLs** – Instantly generate short, shareable links.  
✅ **Custom Short Codes** – Choose a custom alias for your short URL.  
✅ **QR Code Generation** – Get a scannable QR code for every short link.  
✅ **Click Analytics** – Track total clicks and last access timestamps.  
✅ **Fully Responsive UI** – Built with **React & Tailwind CSS**.  
✅ **Cloud Deployment** – Hosted on **Render (backend) and AWS Amplify (frontend)** for scalability.  

---

## 🛠️ Technologies Used  
### **Frontend (React + Vite + TailwindCSS)**  
- React  
- Tailwind CSS  
- Axios (for API calls)  
- React Icons  

### **Backend (Flask + SQLite → PostgreSQL Upgrade Planned)**  
- Flask  
- Flask-SQLAlchemy (ORM for database)  
- Flask-CORS  
- ShortUUID (for short code generation)  
- QRCode (for QR code creation)  
- SQLite (PostgreSQL migration planned)  
- Render (Backend Hosting)  
- AWS Amplify (Frontend Hosting)  

---

## 🌍 Live Deployment
- **Frontend (AWS Amplify):** [Live Demo](https://main.d3fwhdos1eu6vo.amplifyapp.com/)
- **Backend (Render):** [API Base URL](https://shortify-url-shortener-and-qr-code.onrender.com/)

### ⚠️ **Note about Render's Free Tier**  
- The backend **may take a few seconds to spin up** if it hasn’t been used in a while. Please be patient when making requests.  
- The backend **does not have a landing page yet**, so visiting the base Render URL (`/`) will return a `404 Not Found` response.  

---

## 📈 Future Improvements
- 🔹 **Upgrade to PostgreSQL for persistent storage**  
- 🔹 **User authentication & dashboard for managing links**  
- 🔹 **Expiration dates for short URLs**  
- 🔹 **More analytics (location, device tracking, etc.)**  
