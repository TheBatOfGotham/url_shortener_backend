# URL Shortener with FastAPI and MySQL

This is a URL shortener application built with **FastAPI** and **MySQL**. The backend is deployed on **Render**, and the frontend is hosted on **Netlify**. The URL shortening service allows users to shorten long URLs. There is provision to track the usage of shortened URLs. The free instance in Render will spin down with inactivity, which can delay requests by 50 seconds or more.

## Project Structure

```
/app
    ├── main.py        # FastAPI application
    ├── database.py    # Database setup
    ├── models.py      # SQLAlchemy models
    ├── utils.py       # Utility functions (e.g., encoding for short URLs)
    ├── config.py      # Configuration settings (e.g., BASE_URL)
requirements.txt      # Python dependencies
```

### Frontend URL:
[https://urlkunjaakkal.netlify.app/](https://urlkunjaakkal.netlify.app/)

![{6740F062-6DAA-43AA-9547-C18051F95566}](https://github.com/user-attachments/assets/93e2df54-caef-4e89-a79b-9e9e4018fc58)

### Backend URL:
[https://url-shortener-backend-qcmu.onrender.com/](https://url-shortener-backend-qcmu.onrender.com/)

## Setup Instructions

### 1. **Clone the repository:**

```bash
git clone https://github.com/your-repo-url.git
cd your-repo-url
```

### 2. **Install dependencies:**

Ensure that you have Python 3.8+ installed, then install the required Python packages:

```bash
pip install -r requirements.txt
```

### 3. **Configure Environment Variables:**

The application uses a `.env` file to manage configuration variables like the **BASE_URL** and **DATABASE_URL**.

1. Create a `.env` file in the root of your project (if not already present).
2. Add the following variables in the `.env` file:

```env
BASE_URL=http://localhost:8000/       # or your deployed backend URL
DATABASE_URL=mysql://username:password@hostname:port/database_name
```

- Replace `username`, `password`, `hostname`, `port`, and `database_name` with your **Aiven MySQL** credentials.
- Make sure your database is set up before using the backend. You can do this by accessing your **Aiven MySQL** instance and creating the required database. If you're using the default settings, you can just connect with the provided credentials.

### 4. **Run the Backend Locally:**

If you'd like to run the backend locally, use the following command:

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI application on `http://127.0.0.1:8000`.

### 5. **Access the API Documentation:**
   Once the server is running, visit the following URL to access the FastAPI interactive API documentation:

   ```
   http://127.0.0.1:8000/docs
   ```

   This will provide detailed documentation of the available endpoints.

## Available Endpoints

### 1. **POST /shorten**
   - **Purpose**: Shorten a long URL.
   - **Request body**: JSON with `long_url` field containing the URL to be shortened.
   - **Example Request**:
     ```json
     {
       "long_url": "https://www.example.com"
     }
     ```
   - **Response**:
     ```json
     {
       "shortUrl": "https://url-shortener-backend-qcmu.onrender.com/1"
     }
     ```

### 2. **GET /details**
   - **Purpose**: Get details about a URL (either long or short).
   - **Request**: Query parameter `url` (either the long URL or the short URL).
   - **Example Request**: 
     `GET /details?url=https://url-shortener-backend-qcmu.onrender.com/1`
   - **Response**:
     ```json
     {
       "shortUrl": "https://url-shortener-backend-qcmu.onrender.com/1",
       "hitCount": 10
     }
     ```
     
### 3. **GET /{short_code}**
   - **Purpose**: Redirect a short URL to the original long URL.
   - **Request**: Use the short code (e.g., `1`) to access the long URL.
   - **Example Request**: 
     `GET /1`
   - **Response**: Redirects to the long URL (e.g., `https://www.example.com`).

### 4. **GET /top/{number}**
   - **Purpose**: Get the top `n` most visited URLs.
   - **Request**: Path parameter `number` (the number of top URLs to fetch).
   - **Example Request**: 
     `GET /top/5`
   - **Response**:
     ```json
     [
       {
         "longUrl": "https://www.example1.com",
         "shortUrl": "https://url-shortener-backend-qcmu.onrender.com/1",
         "hitCount": 100
       },
       {
         "longUrl": "https://www.example2.com",
         "shortUrl": "https://url-shortener-backend-qcmu.onrender.com/2",
         "hitCount": 50
       }
     ]
     ```

### 5. **GET /docs**
   - **Purpose**: This provides access to the FastAPI auto-generated documentation, where you can test the endpoints.
   - **URL**: 
     [https://url-shortener-backend-qcmu.onrender.com/docs](https://url-shortener-backend-qcmu.onrender.com/docs)

## CORS Configuration

The backend has been configured with **CORS** to allow access from the frontend hosted on **Netlify** at the following URL:
[https://urlkunjaakkal.netlify.app/](https://urlkunjaakkal.netlify.app/)

## Frontend Usage

Visit the frontend at [https://urlkunjaakkal.netlify.app/](https://urlkunjaakkal.netlify.app/), where you can:
- Input a long URL.
- Click "Shorten" to receive the shortened URL.
- Copy the shortened URL to your clipboard.
- Click "Shorten Next" to clear the input and shorten another URL.
