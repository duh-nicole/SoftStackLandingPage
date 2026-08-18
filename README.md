# SoftStack Studios — Onboarding API & Dashboard 🚀

A full-stack project onboarding and pipeline management system built with **FastAPI**, **SQLAlchemy**, and **SQLite**,
paired with an accessible, mobile-responsive dashboard.

---

## ✨ Features

* **Client Onboarding Form:** Responsive client-facing brief submission interface with dynamic feature tag selection.
* **Live Admin Dashboard:** Real-time metrics grid tracking total active briefs and estimated pipeline revenue.
* **WCAG-Compliant Accessibility:** Full keyboard navigation support (`Tab`, `Enter`, `Space`), `aria-modal` dialogs,
  and keyboard focus trapping.
* **Dark & Light Mode:** Built-in CSS custom properties supporting seamless system/manual theme switching.
* **Automated Data Sync:** Upserts client profile updates automatically upon brief re-submission.

---

## 🛠️ Tech Stack

* **Backend:** FastAPI, Python 3.10+
* **ORM & Database:** SQLAlchemy, SQLite
* **Data Validation:** Pydantic (v2)
* **Frontend:** Vanilla HTML5, CSS3 (Custom Variables & Grid/Flexbox), JavaScript (ES6+ Fetch API)

---

## 📁 Project Structure

```text
.
├── database.py       # SQLite engine, session local setup, and get_db dependency
├── models.py         # SQLAlchemy models (Client, ProjectBrief)
├── main.py           # FastAPI router, CORS middleware, schemas, & endpoints
├── index.html        # Client-facing onboarding brief submission form
├── dashboard.html    # Admin dashboard for reviewing submitted briefs
├── dashboard.js      # Dashboard state management, modal logic & focus trap
└── styles.css        # Shared design tokens, theme vars, and responsive layouts

---

⚙️ Getting Started
1. Clone the Repository & Navigate in Terminal

```bash
git clone <https://github.com/duh-nicole/SoftStackLandingPage>
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

The server will spin up locally at http://127.0.0.1:8000. 
The SQLite database (onboarding.db) will automatically generate on launch!

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
   
