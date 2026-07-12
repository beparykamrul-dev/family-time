# ISP-OS (Internet Service Provider Operating System)

A complete ISP management system with frontend and backend.

## Project Structure

```
family-time/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── context/      # Context providers (Auth, Theme, Language)
│   │   ├── pages/        # Page components
│   │   ├── i18n/         # Translations
│   │   ├── mock/         # Mock data
│   │   ├── App.jsx       # Main app
│   │   └── main.jsx      # Entry point
│   ├── package.json
│   └── vite.config.js
├── backend/              # Flask backend
│   ├── app.py           # Main application
│   ├── requirements.txt
│   └── README.md
└── README.md
```

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Features

✅ **Dashboard** - Stats, revenue charts, network map, alerts  
✅ **Customers** - Manage customer database  
✅ **Invoices** - Track billing and payments  
✅ **OLTs** - Manage optical line terminals  
✅ **Devices** - Monitor ONUs and devices  
✅ **Authentication** - JWT-based login system  
✅ **Dark Mode** - Toggle between light/dark themes  
✅ **Multi-language** - Bengali & English support  
✅ **Responsive Design** - Mobile, tablet, desktop  
✅ **API Integration** - RESTful backend API  

## Demo Credentials

```
Email: admin@example.com
Password: password123
```

## Technologies

**Frontend:**
- React 18
- React Router
- Tailwind CSS
- Recharts (Charts)
- Leaflet (Maps)
- Lucide Icons
- Axios

**Backend:**
- Flask
- PyJWT
- Flask-CORS

## License

MIT
