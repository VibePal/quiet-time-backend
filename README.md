# Quiet Time API - Backend

FastAPI backend for the Quiet Time Application with PostgreSQL database integration.

## Features

- 🔐 Admin authentication with JWT tokens
- 📝 CRUD operations for quiet time entries
- 🗄️ PostgreSQL database integration
- 🔒 Protected admin routes
- 📖 Public API for viewing entries

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip (Python package manager)

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment Variables**
   
   Create a `.env` file in the root directory with the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/quiettime_db
   SECRET_KEY=your-secret-key-here-change-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ```

3. **Initialize Database**
   
   The database tables will be created automatically when you run the application. To create the admin user, run:
   ```bash
   python init_admin.py
   ```
   
   This will create an admin user with:
   - Username: `admin`
   - Password: `password`

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive API docs: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

## API Endpoints

### 1. Admin Login
**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**
```json
{
  "username": "admin",
  "password": "hfcc2024"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "username": "admin"
    }
  }
}
```

### 2. Add New Quiet Time Entry
**Endpoint:** `POST /api/v1/quiet-time/entries`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "song": {
    "title": "Amazing Grace",
    "youtubeId": "CD-E-LDc384"
  },
  "scripture": {
    "reference": "Psalm 23:1-6",
    "text": "The Lord is my shepherd; I shall not want..."
  },
  "prayer": {
    "title": "Prayer for Peace",
    "content": "Lord, grant us peace in our hearts and minds today..."
  }
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Quiet time entry added successfully",
  "data": {
    "id": "1",
    "song": {...},
    "scripture": {...},
    "prayer": {...},
    "createdAt": "2025-10-10T12:34:56.789Z"
  }
}
```

### 3. Get Today's Entry (Daily Rotation)
**Endpoint:** `GET /api/v1/quiet-time/entries/today`

**No authentication required**

This endpoint automatically rotates through all entries, showing a different one each day. When it reaches the end, it cycles back to the beginning.

**Success Response (200):**
```json
{
  "success": true,
  "message": "Today's entry retrieved successfully",
  "data": {
    "id": "1",
    "song": {...},
    "scripture": {...},
    "prayer": {...},
    "createdAt": "2025-10-10T12:34:56.789Z",
    "updatedAt": "2025-10-10T14:20:30.123Z"
  }
}
```

### 4. Get All Quiet Time Entries
**Endpoint:** `GET /api/v1/quiet-time/entries`

**No authentication required**

**Success Response (200):**
```json
{
  "success": true,
  "message": "Entries retrieved successfully",
  "data": [...]
}
```

### 5. Update Quiet Time Entry
**Endpoint:** `PATCH /api/v1/quiet-time/entries/{entry_id}`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "song": {
    "title": "Amazing Grace (Updated)",
    "youtubeId": "NEW_VIDEO_ID"
  },
  "scripture": {
    "reference": "Psalm 23:1-6",
    "text": "Updated scripture text..."
  },
  "prayer": {
    "title": "Updated Prayer Title",
    "content": "Updated prayer content..."
  }
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Entry updated successfully",
  "data": {
    "id": "1",
    "song": {...},
    "scripture": {...},
    "prayer": {...},
    "createdAt": "2025-10-10T12:34:56.789Z",
    "updatedAt": "2025-10-10T14:20:30.123Z"
  }
}
```

### 6. Delete Quiet Time Entry
**Endpoint:** `DELETE /api/v1/quiet-time/entries/{entry_id}`

**Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Entry removed successfully",
  "data": null
}
```

## Project Structure

```
QuietTime-Backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       └── quiet_time.py    # Quiet time entry routes
├── init_admin.py            # Admin initialization script
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (create this)
└── README.md
```

## Database Schema

### Admin Table
- `id`: Integer (Primary Key)
- `username`: String (Unique)
- `hashed_password`: String
- `created_at`: DateTime

### Quiet Time Entries Table
- `id`: Integer (Primary Key)
- `song_title`: String
- `song_youtube_id`: String
- `scripture_reference`: String
- `scripture_text`: Text
- `prayer_title`: String
- `prayer_content`: Text
- `created_at`: DateTime

## Security

- Passwords are hashed using bcrypt
- JWT tokens expire after 7 days (configurable)
- Admin-only routes are protected with JWT authentication
- CORS is configured (update for production)

## Development

The application uses:
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation
- **python-jose**: JWT token handling
- **passlib**: Password hashing

## Production Deployment

Before deploying to production:

1. Update CORS origins in `app/main.py`
2. Change the `SECRET_KEY` in `.env` to a secure random string
3. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
4. Set up proper database backups
5. Use environment variables for sensitive data
6. Enable HTTPS

## Troubleshooting

**Database Connection Issues:**
- Verify your `DATABASE_URL` is correct
- Ensure PostgreSQL is running
- Check database credentials and permissions

**Admin Login Not Working:**
- Run `python init_admin.py` to create the admin user
- Check if the database tables were created

**CORS Issues:**
- Update the `allow_origins` in `app/main.py` with your frontend URL

## License

This project is for HFCC 2024.

