# BlueScope Steel Inventory Management API

A FastAPI-based inventory management system for steel products with a modern web interface.

## Setup

```powershell
python -m venv venv
. .\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m uvicorn app.main:app --reload
```

## Access the Application

- **Web Interface:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Alternative API Docs:** http://localhost:8000/redoc

## Features (Partial Implementation)

- ✅ Modern web interface with real-time inventory display
- ✅ Dashboard with statistics
- ✅ Product filtering and search
- [ ] CRUD operations for steel inventory (basic implementation)
- [ ] Weight and dimension calculations
- [ ] Inventory level alerts
- [ ] Grade specifications
- [ ] Batch tracking

## Sample Data

The application comes pre-loaded with 10 steel products across different:
- **Shapes:** Sheet, Coil, Plate, Bar, Tube
- **Grades:** A36, 304, 316, 4140
- **Locations:** Warehouse-A, Warehouse-B, Warehouse-C
