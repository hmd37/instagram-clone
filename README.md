# 📸 Instagram Clone API

A Django REST Framework (DRF) API that replicates core Instagram features such as user authentication, posts, likes, comments, and follow/unfollow functionality.

## 🚀 Features

✅ User Authentication (Register, Login, JWT)  
✅ Create, Read, Update, and Delete (CRUD) for Posts  
✅ Like/Unlike Posts  
✅ Comment on Posts  
✅ Follow/Unfollow Users  
✅ User Profiles with Followers & Following Counts  
✅ Search Users  

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework  
- **Database**: PostgreSQL  
- **Authentication**: JWT (JSON Web Tokens)  
- **Documentation**: DRF Spectacular (OpenAPI/Swagger)  

## 📦 Installation

1️⃣ **Clone the Repository**  


2️⃣ **Create a Virtual Environment & Install Dependencies**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Configure Environment Variables**  
Create a `.env` file in the root directory and add the required variables:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

4️⃣ **Apply Migrations & Create Superuser**  
```bash
python manage.py migrate
python manage.py createsuperuser
```

5️⃣ **Run the Development Server**  
```bash
python manage.py runserver
```

## 🔑 Authentication

- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`
- **Get User Profile**: `GET /api/users/{username}/`
- **Update Profile**: `PUT /api/users/{username}/`
- **Follow/Unfollow**: `POST /api/users/{username}/follow/`

## 🖼️ Posts & Interactions

- **Create Post**: `POST /api/posts/`
- **Retrieve Post**: `GET /api/posts/{post_id}/`
- **Like/Unlike Post**: `POST /api/posts/{post_id}/like/`
- **Comment on Post**: `POST /api/posts/{post_id}/comment/`

## 📜 API Documentation

After running the server, access the API documentation at:  
🔗 `http://127.0.0.1:8000/api/schema/swagger-ui/`  

## 🤝 Contributing

Contributions are welcome! Feel free to fork, create a pull request, or open an issue. 🚀
