# Omniscient Market Tracker

<div align="center">

![Omniscient Logo](https://img.shields.io/badge/Omniscient-Market%20Intelligence-blue?style=for-the-badge)

**AI-Powered Sales Trend Tracker & Market Intelligence Dashboard**

Monitor market velocity, sell-through rates, and emerging opportunities across e-commerce and community platforms.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16.1-black.svg)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19.2-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Tech Stack](#️-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [💻 Usage](#-usage)
- [🔗 API Reference](#-api-reference)
- [⚙️ Configuration](#️-configuration)
- [🎯 Watchlist Items](#-watchlist-items)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🎯 Project Overview

The **Omniscient Market Tracker** is a professional-grade market intelligence platform that analyzes digital footprints across e-commerce and community platforms to infer real-time market demand. By combining eBay's market data with Reddit's community sentiment, the system identifies emerging trends, calculates sell-through rates, and scores market opportunities.

**Project Philosophy**: Market demand leaves digital footprints. We track these signals to provide actionable intelligence for sellers, traders, and market analysts.

---

## ✨ Key Features

### 📊 **Market Analytics**
- **Sell-Through Rate (STR) Analysis**: Real-time calculation of supply vs. demand ratios
- **Momentum Tracking**: 7-day and 30-day moving averages with trend classification
- **Price Intelligence**: Standard deviation analysis with outlier detection
- **Opportunity Scoring**: 0-100 scoring system for market opportunities

### 🔍 **Multi-Platform Monitoring**
- **eBay Velocity Probe**: Scrapes active listings, sold items, and pricing data
- **Reddit Reality Scanner**: Analyzes community demand and hiring patterns
- **Real-time WebSocket Feed**: Live market signals and alerts

### 📈 **Predictive Analytics**
- **Trend Classification**: `STRONG_UP`, `FLAT`, or `DOWN` trend detection
- **Anomaly Detection**: Identifies market spikes and unusual patterns
- **Forecasting**: EMA-based future STR predictions
- **Signal Generation**: Automated alerts for critical market events

### 🎨 **Interactive Dashboard**
- **Real-time Visualizations**: Built with Recharts and Tailwind CSS
- **Category Heatmaps**: Visual representation of market activity by category
- **Historical Trends**: Time-series analysis and pattern recognition
- **Responsive Design**: Works seamlessly across desktop and mobile devices

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Sources  │    │  Analytics      │    │   Frontend      │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │   eBay API  │ │    │ │  Trend      │ │    │ │  Next.js    │ │
│ └─────────────┘ │    │ │  Engine     │ │    │ │  Dashboard  │ │
│                 │    │ └─────────────┘ │    │ └─────────────┘ │
│ ┌─────────────┐ │    │                 │    │                 │
│ │  Reddit     │ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │  Scraping   │ │    │ │  Anomaly    │ │    │ │  Real-time  │ │
│ └─────────────┘ │    │ │  Detector  │ │    │ │  Updates    │ │
│                 │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    │                 │    │                 │
                       │ ┌─────────────┐ │    │ ┌─────────────┐ │
                       │ │  Forecaster │ │    │ │  WebSocket  │ │
                       │ └─────────────┘ │    │ │  Client     │ │
                       │                 │    │ └─────────────┘ │
                       └─────────────────┘    └─────────────────┘
                                ↓
                       ┌─────────────────┐
                       │  FastAPI Layer │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │  REST API   │ │
                       │ └─────────────┘ │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │  WebSocket  │ │
                       │ └─────────────┘ │
                       └─────────────────┘
                                ↓
                       ┌─────────────────┐
                       │   SQLite DB    │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │  Market     │ │
                       │ │  Stats      │ │
                       │ └─────────────┘ │
                       │                 │
                       │ ┌─────────────┐ │
                       │ │  Signals    │ │
                       │ └─────────────┘ │
                       └─────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: Python SQL toolkit and ORM
- **SQLite**: Lightweight database for data persistence
- **BeautifulSoup4**: Web scraping library
- **Requests**: HTTP library for API calls
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI

### Frontend
- **Next.js 16.1**: React framework with App Router
- **React 19.2**: User interface library
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS 4**: Utility-first CSS framework
- **Recharts**: Composable charting library
- **Lucide React**: Beautiful & consistent icon toolkit

### Development Tools
- **PowerShell**: Cross-platform task automation
- **ESLint**: JavaScript and TypeScript linter
- **Babel**: JavaScript compiler

---

## 🚀 Quick Start

### One-Click Launch (Windows)
```powershell
# Navigate to project directory
cd C:\sales\omniscient-tracker

# Launch everything at once
.\start_app.ps1
```

This script will:
1. Install Python backend dependencies
2. Install Node.js frontend dependencies
3. Start the backend server on port 8000
4. Start the frontend development server on port 4303
5. Open your browser to `http://localhost:4303`

---

## 📦 Installation

### Prerequisites
- **Python 3.8+** installed and in PATH
- **Node.js 18+** installed and in PATH
- **PowerShell** (for Windows launch script)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev -- -p 4303
   ```

   The frontend will be available at `http://localhost:4303`

---

## 💻 Usage

### Dashboard Features

1. **Market Overview**: View global market velocity and health indicators
2. **Trend Leaders**: Explore items with highest sell-through rates
3. **Category Analysis**: Filter and analyze by Electronics, Gaming, Fashion, Collectibles, or Tools
4. **Real-time Alerts**: Receive WebSocket notifications for market anomalies
5. **Historical Analysis**: Track price trends and volume patterns over time

### API Interaction

Access the interactive API documentation at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### WebSocket Connection

Connect to the live WebSocket feed for real-time market signals:
```javascript
const ws = new WebSocket('ws://localhost:8000/api/ws/live');
ws.onmessage = (event) => {
    const signal = JSON.parse(event.data);
    console.log('Market Signal:', signal);
};
```

---

## 🔗 API Reference

### Core Data Endpoints

#### Get System Health
```http
GET /
```
Returns system status and version information.

#### Get Current Trends
```http
GET /api/trends
```
Triggers parallel scanning of the eBay watchlist and returns analyzed market data with opportunity scores.

#### Get Platform Metrics
```http
GET /api/platforms
```
Scans Reddit for community-driven demand metrics and platform saturation ratios.

#### Get System Pulse
```http
GET /api/pulse
```
Returns system-wide health metrics and global velocity indices.

#### Get Market Signals
```http
GET /api/signals
```
Retrieves generated market signals and alerts from the monitoring system.

### Analytics Endpoints

#### Get Historical Data
```http
GET /api/history/item/{keyword}
GET /api/history/market
```
Access historical market statistics and trends.

#### Get Forecast
```http
GET /api/analytics/forecast/{keyword}
```
Retrieve EMA-based future predictions for specific items.

#### Get Anomalies
```http
GET /api/analytics/anomalies
```
Identify market spikes and unusual patterns.

#### Get Opportunities
```http
GET /api/analytics/opportunities
```
Get scored market opportunities with recommendations.

#### Get Heatmap Data
```http
GET /api/analytics/heatmap
```
Retrieve category-wise market activity data for visualization.

### Real-time WebSocket

#### Live Market Feed
```http
WS /api/ws/live
```
Connect for real-time market signals and critical alerts.

---

## ⚙️ Configuration

### Environment Variables

The system uses environment variables for configuration. Create a `.env` file in the backend directory:

```env
# Database Configuration
DATABASE_URL=sqlite:///./market_intelligence.db

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000

# Logging Level
LOG_LEVEL=INFO

# Reddit API (Optional - for enhanced Reddit data)
# REDDIT_CLIENT_ID=your_client_id
# REDDIT_CLIENT_SECRET=your_client_secret
# REDDIT_USER_AGENT=OmniscientMarketTracker/1.0
```

### CORS Configuration

The backend is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:4303`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:4303`

Modify the `origins` list in `backend/main.py` to add additional allowed origins.

---

## 🎯 Watchlist Items

The system currently tracks **20+ items across 5 categories**:

### 🖥️ Electronics
- Vintage Digital Camera
- Fujifilm X100V
- Sony Walkman
- Flipper Zero
- Nvidia RTX 4090

### 🎮 Gaming
- Steam Deck OLED
- Analogue Pocket
- Nintendo 3DS XL

### 👕 Fashion
- Carhartt Detroit Jacket
- Arc'teryx Beta LT
- Birkenstock Boston
- Onitsuka Tiger Mexico 66

### 🏺 Collectibles
- Sonny Angel
- Jellycat Plush
- One Piece TCG Booster
- Lego Rivendell

### 🔧 Tools
- Leatherman Arc
- Knipex Cobra XS
- Yeti Rambler

### Subreddits Monitored
- r/forhire
- r/freelance_forhire
- r/hardwareswap
- r/mechmarket
- r/photomarket

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** with proper testing
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- **Code Style**: Follow PEP 8 for Python and use ESLint for JavaScript/TypeScript
- **Testing**: Ensure all new features include appropriate tests
- **Documentation**: Update relevant documentation for API changes
- **Commit Messages**: Use clear, descriptive commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **FastAPI** team for the excellent web framework
- **Next.js** team for the React framework
- **eBay** for providing market data
- **Reddit** community for valuable insights
- **Recharts** team for the visualization library

---

<div align="center">

**Built with ❤️ by the Omniscient Team**

[🌐 Live Demo](https://github.com/alrightryanx/trendySales) • [📚 Documentation](docs/) • [🐛 Report Issues](issues)

</div>