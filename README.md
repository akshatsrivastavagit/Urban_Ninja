# 🛠️ UrbanClap Clone – Home Service Booking Web App

This is a full-stack clone of **UrbanClap**, offering a multi-role platform where users can book home services, technicians manage assignments, and admins control operations. It includes detailed workflows, real-time booking, payment gateway integration, dashboards, and user feedback systems.

---

## 🚀 Features

### 👤 Client Portal

- Check service availability by city.
- Sign in via Google OAuth.
- Browse categories → subcategories → service packages.
- Add services to cart, adjust quantities, and proceed to checkout.
- Pay using Razorpay.
- Track past bookings, download bills, leave reviews, and cancel services.
- Auto-credit handling for cancellations and applied discounts.

### 🛠️ Technician Portal

- Login via email.
- View assigned jobs.
- Confirm job completion with OTP from customer.

### 🧑‍💼 Admin Portal

- Secure login via company key.
- Dashboard: sales, revenue, top services, booking trends.
- Payment reconciliation with UPI reference.
- View full database.
- Monitor technician performance and earnings.

---

## 🖼️ Screenshots & Workflow Images

Replace the `your-username` in URLs with your actual GitHub username if needed.

### 1. 🔍 Home Page – Check City Availability

![Screenshot 2025-06-03 032812](https://github.com/user-attachments/assets/4b46b606-3d4c-44e8-a6b3-ca59c1096908)

### 2. 🔐 Google OAuth Login Flow

![Screenshot 2025-06-03 032836](https://github.com/user-attachments/assets/9de30e14-e8ea-4c40-af71-7f33336e5001)  
![Screenshot 2025-06-03 032847](https://github.com/user-attachments/assets/f9773ec9-9179-4319-ad15-33c7a767fc9b)

### 3. 📚 Browse Services by Category and Subcategory

![Screenshot 2025-06-03 032914](https://github.com/user-attachments/assets/d81158d1-20fe-41d1-8007-a541f50da630)  
![Screenshot 2025-06-03 032924](https://github.com/user-attachments/assets/dede9bc6-16a0-4857-aa10-2e4e4546ed62)

### 4. 🛒 Add to Cart and View Cart

![Screenshot 2025-06-03 032943](https://github.com/user-attachments/assets/3fa6ff60-8993-4d94-bb5d-0b84092f9f4a)  
![Screenshot 2025-06-03 033001](https://github.com/user-attachments/assets/4e374536-c650-406f-953e-a5580f482461)

### 5. 📅 Slot Selection & Address Form

![Screenshot 2025-06-03 031253](https://github.com/user-attachments/assets/f6edd616-3345-4c44-bca6-f7ffb358a0f1)  
![Screenshot 2025-06-03 031313](https://github.com/user-attachments/assets/f562009d-facf-466d-be8a-8b76065ed06f)  
![Screenshot 2025-06-03 031401](https://github.com/user-attachments/assets/664cc972-fb87-4f60-a37c-9e9bda5bfc6e)

### 6. 💳 Razorpay Payment Gateway

![Screenshot 2025-06-03 031412](https://github.com/user-attachments/assets/4c25bbac-4e5a-42b2-920d-9462b340b50f)  
![Screenshot 2025-06-03 031432](https://github.com/user-attachments/assets/b7cf6fe0-6083-4d84-83eb-2d0aaafb13ed)  
![Screenshot 2025-06-03 031455](https://github.com/user-attachments/assets/d9553a62-dd80-4bf5-bf2e-dd7d9a9dc42f)

### 7. 📜 Booking Summary & Bill Generation

![Screenshot 2025-06-03 031521](https://github.com/user-attachments/assets/7d68e1ad-438d-48e0-8545-b0f1fcffb138)  
![Screenshot 2025-06-03 031619](https://github.com/user-attachments/assets/3fc217f5-6faa-46d7-aa19-f2632daea6e7)  
![Screenshot 2025-06-03 031627](https://github.com/user-attachments/assets/37d74c02-35a4-4692-9b72-f161a9d53893)

### 8. ✍️ Review and Feedback Submission

![Screenshot 2025-06-03 033019](https://github.com/user-attachments/assets/55ab7ff0-a84d-4e35-b11d-85b80803f40f)

### 9. 👨‍🔧 Technician Portal – View Assigned Jobs

![Screenshot 2025-06-03 033338](https://github.com/user-attachments/assets/ba6fa8cd-233e-4fcf-89aa-27542462f79d)  
![Screenshot 2025-06-03 033359](https://github.com/user-attachments/assets/d185bb60-0353-4c12-8243-b25a1e269d78)

### 10. 📊 Admin Dashboard – Charts & Analytics

![Screenshot 2025-06-03 033058](https://github.com/user-attachments/assets/32ced892-603a-4d8a-8d74-98fe26cec3f8)  
![Screenshot 2025-06-03 033153](https://github.com/user-attachments/assets/fc91e852-fe31-4c4d-b2dc-0d261b62834b)  
![Screenshot 2025-06-03 033211](https://github.com/user-attachments/assets/658ff2df-3081-443b-82dc-6d872a51eb41)  
![Screenshot 2025-06-03 033226](https://github.com/user-attachments/assets/87dcf57b-dc2f-4aa8-b58c-568a9e6b532f)

### 11. 💰 Admin – Payment Management

![Screenshot 2025-06-03 033110](https://github.com/user-attachments/assets/0ba80802-bb6c-4218-9a43-13494e39a87a)

### 12. 🧾 Show Full Database

![Screenshot 2025-06-03 042752](https://github.com/user-attachments/assets/9d1b09d3-e737-4ead-bf44-eb43bb747556)

---

## 📁 Project Structure

```
urbanclap-clone/
│
├── app.py
├── config.py
├── requirements.txt
├── templates/
├── static/
│   └── images/
└── SQL/
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/urbanclap-clone.git
   cd urbanclap-clone
   ```

2. **Create virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL**
   - Create a DB named `group-project-1`
   - Import SQL files from the `/SQL` folder

5. **Run the app**
   ```bash
   python app.py
   ```

---

## 🔐 Tech Stack

- **Backend**: Python (Flask), MySQL
- **Frontend**: HTML, Bootstrap, Jinja2
- **Auth**: Google OAuth via Authlib
- **Payments**: Razorpay API
- **Charts**: Chart.js

---

## 👨‍💻 Author

- **Akshat Srivastava** – Full Stack Developer

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 💬 Feedback

Feel free to [open issues](https://github.com/your-username/urbanclap-clone/issues) or submit pull requests. Contributions are welcome!
