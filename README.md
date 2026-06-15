# 🏠 RentSearch — Live Rental Property Finder

A full-stack web application for searching real rental listings across the US, powered by live Zillow data.

🔗 **Live App**: https://housing-market-analyzer.streamlit.app

## Features
- 🔍 Search by city, neighborhood, or ZIP code
- 💰 Filter by rent range, bedrooms, pet policy, home type
- 📅 Filter by move-in date and search radius
- 📊 Live KPI summary — avg, lowest, and highest rent
- 🏷️ Zillow estimate comparison on every listing
- 🔗 Direct links to full Zillow listing pages

## Tech Stack
- **Python** — core application logic
- **Streamlit** — web framework and UI
- **RapidAPI / Zillow API** — live rental listing data
- **python-dotenv** — secure API key management

## Setup

1. Clone the repo
```bash
   git clone https://github.com/Sadiazaman067/housing-market-analyzer.git
   cd housing-market-analyzer
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file with your RapidAPI key
RAPIDAPI_KEY=your_key_here

4. Run the app
```bash
   streamlit run dashboard.py
```

## Project Structure
```
housing-market-analyzer/
├── dashboard.py       # Main application
├── requirements.txt   # Dependencies
├── .gitignore         # Excludes .env and cache files
└── README.md          # Project documentation
```

## Data Source
Live rental listings sourced from Zillow via the Private-Zillow API on RapidAPI.
For informational purposes only.