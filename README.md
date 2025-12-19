# Frontend - Streamlit User Management Portal

This is the Streamlit frontend application for the Astrology Booklet User Management system.

## Features

- **View All Users**: List all users in the database
- **Get User by ID**: Retrieve specific user information
- **Create/Update User**: Add new users or update existing ones
- **Get Astrology Placements**: View complete astrology placements for a user
- **Get Big Three**: View Sun, Moon, and Ascendant signs
- **Generate Booklet PDF**: Create astrology booklet PDFs
- **Generate Calendar PDF**: Create calendar PDFs for a specific year

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
export API_BASE_URL=http://localhost:8010
```

3. Run the Streamlit app:
```bash
streamlit run app.py
```

## Configuration

- **API Base URL**: Configure the FastAPI backend URL in the sidebar
- **Bearer Token**: Optional authentication token if your backend requires it

## Deployment to Streamlit Cloud

1. Push this frontend directory to your GitHub repository
2. Connect your repository to Streamlit Cloud
3. Set the root directory to `frontend/`
4. Set the main file to `app.py`
5. Add environment variables if needed:
   - `API_BASE_URL`: Your deployed FastAPI backend URL

## Backend Connection

This frontend connects to the FastAPI backend running in the `backend/` directory. Make sure the backend is running and accessible at the configured URL.

