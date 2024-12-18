from fastapi import FastAPI, Depends, HTTPException
from fastapi import Query
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models import URL,URLRequest
from app.database import engine, Base, get_db
from app.utils import encode_base62, is_rate_limited
from app.config import BASE_URL

app = FastAPI()

# Allow CORS from localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://polite-kheer-57244b.netlify.app"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # All HTTP methods
    allow_headers=["*"],  # All headers
)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

# Constants
AD_REDIRECT_URL = "https://www.google.com"

@app.post("/shorten")
def create_short_url(url_request: URLRequest, db: Session = Depends(get_db)):
    long_url = url_request.long_url  # Access the long_url from the request body

    existing_url = db.query(URL).filter(URL.long_url == long_url).first()
    if existing_url:
        return {"shortUrl": existing_url.short_url}

    # Create new URL entry
    new_url = URL(long_url=long_url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    # Generate short URL
    short_code = encode_base62(new_url.id)
    new_url.short_url = f"{BASE_URL}{short_code}"
    db.commit()

    return {"shortUrl": new_url.short_url}

@app.get("/details")
def get_url_details(url: str = Query(...), db: Session = Depends(get_db)):
    base_url = BASE_URL
    print(url)
    
    if url.startswith(base_url):  # It's a short URL
        short_url = url
        url_entry = db.query(URL).filter(URL.short_url == short_url).first()
        
        if not url_entry:
            raise HTTPException(status_code=404, detail="Short URL not found")
        
        return {
            "hitCount": url_entry.hit_count
        }
    else:  # It's a long URL
        url_entry = db.query(URL).filter(URL.long_url == url).first()
        
        if not url_entry:
            raise HTTPException(status_code=404, detail="Long URL not found")
        
        return {
            "shortUrl": url_entry.short_url,
            "hitCount": url_entry.hit_count
        }

@app.get("/{short_code}")
def redirect_to_long_url(short_code: str, db: Session = Depends(get_db)):
    short_url = f"{BASE_URL}{short_code}"
    url_entry = db.query(URL).filter(URL.short_url == short_url).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found hehehe")

    # Check rate limit
    if is_rate_limited(url_entry):
        raise HTTPException(status_code=429, detail="Daily request limit reached")

    # Increment hit count
    url_entry.hit_count += 1
    db.commit()

    # Redirect to advertisement on every 10th hit
    if url_entry.hit_count % 10 == 0:
        return RedirectResponse(url=AD_REDIRECT_URL)

    return RedirectResponse(url=url_entry.long_url)        

@app.get("/top/{number}")
def get_top_urls(number: int, db: Session = Depends(get_db)):
    top_urls = db.query(URL).order_by(URL.hit_count.desc()).limit(number).all()
    return [{"longUrl": url.long_url, "shortUrl": url.short_url, "hitCount": url.hit_count} for url in top_urls]