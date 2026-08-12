# SoftStack Studios — Onboarding API & Dashboard 🚀

A full-stack project onboarding system built with **FastAPI**, **SQLAlchemy**, and **SQLite**, paired with a clean HTML/CSS frontend and admin dashboard.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI
* **Database ORM:** SQLAlchemy
* **Database Engine:** SQLite
* **Data Validation:** Pydantic (v2)
* **Frontend:** Plain HTML, CSS, JavaScript (Fetch API)

---

## 📁 Project Structure

```text
.
├── database.py       # SQLite engine, session local setup, and get_db dependency
├── models.py         # SQLAlchemy models (Client, ProjectBrief)
├── main.py           # FastAPI router, CORS middleware, schemas, & endpoints
├── index.html        # Client-facing onboarding brief submission form
├── dashboard.html    # Admin dashboard for reviewing submitted briefs
└── styles.css        # Shared styling across form and dashboard

---

⚙️ Getting Started
1. Clone the Repository & Navigate in Terminal
```bash
git clone <your-repository-url>
cd softstack-onboarding
```
2. Set Up a Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy pydantic[email]
```

4. Run the API Server
```bash
uvicorn main:app --reload
```

The server will spin up locally at http://127.0.0.1:8000. The SQLite database (onboarding.db) will automatically generate on launch!

---

## 🔌 API Endpoints
Method	    # Endpoint	              # Description
├──POST	    # /api/v1/onboarding	    # Submits client profile and project brief. Automatically syncs existing client updates.
├──GET	    # /api/v1/briefs	        # Fetches all submitted briefs with attached client info for the dashboard.

---

## 📖 Interactive Documentation
Once the server is running, visit:
Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc


---
   
