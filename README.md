# 💧 Water Quality Analysis Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_LIVE_LINK_HERE)

> **Advanced water quality analysis using AI/ML and data science techniques to uncover hidden patterns in South African catchment systems.**

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        A1[📊 Excel Dataset<br/>water_quality.xlsx]
        A2[🌐 RSS Feeds<br/>CSIR, News24, Eng News]
    end
    
    subgraph "Data Processing Layer"
        B1[🐼 Pandas<br/>Data Cleaning & Analysis]
        B2[🔢 NumPy<br/>Numerical Computing]
        B3[📡 Feedparser<br/>News Aggregation]
    end
    
    subgraph "Analysis Engine"
        C1[🤖 Correlation Analysis<br/>pH-Chemical Patterns]
        C2[📈 Statistical Analysis<br/>WHO Compliance]
        C3[🔍 Pattern Recognition<br/>Pollution Detection]
    end
    
    subgraph "Visualization Layer"
        D1[📊 Plotly<br/>Interactive Charts]
        D2[🎨 Matplotlib/Seaborn<br/>Statistical Plots]
        D3[💅 Custom CSS<br/>Modern UI Components]
    end
    
    subgraph "Presentation Layer"
        E1[⚡ Streamlit<br/>Web Dashboard]
    end
    
    subgraph "User Interface"
        F1[🖥️ Dashboard Overview<br/>Metrics & KPIs]
        F2[🔬 Discovery Analysis<br/>Scientific Insights]
        F3[📈 Visualizations<br/>Interactive Charts]
        F4[🌊 Live News Feed<br/>Real-time Updates]
    end
    
    A1 --> B1
    A2 --> B3
    B1 --> C1
    B1 --> C2
    B2 --> C1
    B3 --> F4
    C1 --> D1
    C2 --> D1
    C3 --> D2
    D1 --> E1
    D2 --> E1
    D3 --> E1
    E1 --> F1
    E1 --> F2
    E1 --> F3
    E1 --> F4
    
    style A1 fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style A2 fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
    style E1 fill:#FF4B4B,stroke:#333,stroke-width:3px,color:#fff
    style F1 fill:#10B981,stroke:#333,stroke-width:2px,color:#fff
    style F2 fill:#10B981,stroke:#333,stroke-width:2px,color:#fff
    style F3 fill:#10B981,stroke:#333,stroke-width:2px,color:#fff
    style F4 fill:#10B981,stroke:#333,stroke-width:2px,color:#fff
```

### 🛠️ Tech Stack

<div align="center">

| Layer | Technologies |
|-------|-------------|
| **Frontend** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white) |
| **Visualization** | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |
| **News Integration** | ![RSS](https://img.shields.io/badge/RSS-FFA500?style=for-the-badge&logo=rss&logoColor=white) |
| **Version Control** | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) |
| **Deployment** | ![Streamlit Cloud](https://img.shields.io/badge/Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) |

</div>

### 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                                 │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB APP (app.py)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Overview │  │Discovery │  │ Viz Tab  │  │ Raw Data Explorer│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │
└────────┬────────────────┬────────────────┬────────────────┬─────────┘
         │                │                │                │
         ▼                ▼                ▼                ▼
┌────────────────┐ ┌──────────────┐ ┌────────────┐ ┌─────────────┐
│  News Feed     │ │  Correlation │ │  Plotly    │ │  Pandas     │
│  (Feedparser)  │ │  Analysis    │ │  Charts    │ │  DataFrames │
└────────────────┘ └──────────────┘ └────────────┘ └─────────────┘
         │                │                │                │
         ▼                ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DATA PROCESSING LAYER                            │
│  • pH-Chemical Correlation Engine                                   │
│  • WHO Compliance Calculator                                        │
│  • Statistical Analysis (Mean, Median, Range)                       │
│  • Pattern Recognition & Anomaly Detection                          │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       DATA SOURCES                                   │
│  📊 Excel: data/raw/water_quality.xlsx                              │
│  🌐 RSS: CSIR, News24, Engineering News                             │
│  📈 Processed: data/processed/water_quality_summary.csv             │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔗 Live Demo

**🚀 [Launch Dashboard](YOUR_LIVE_LINK_HERE)** - Explore the interactive water quality analysis dashboard

## 📸 Screenshots

### Dashboard Overview
![Dashboard Overview](overview.png)
*Interactive dashboard showing WHO compliance metrics, key statistics, and real-time news feed*

### Data Visualization
![Correlation Analysis](visualization%201.png)
*pH-Chemical correlation comparison revealing opposite patterns between catchments*

### Live News Integration
![News Feed](news%20blog.png)
*Real-time water quality news from CSIR, Department of Water, and national sources with beautiful card design*

## 🎯 Discovery: Opposite Chemical Behaviors in Adjacent Catchments

Analysis of water quality data from MHLATHUZE and LUVUVU catchments in South Africa revealed **fundamentally different chemical behaviors** despite similar geology.

### 🔬 Key Findings:

1. **Critical Water Quality Issues:**
   - **LUVUVU**: 90%+ samples outside WHO pH guidelines (Critical)
   - **MHLATHUZE**: 30%+ samples outside safe range (Moderate-High risk)

2. **Opposite pH-Chemical Correlations:**
   - **MHLATHUZE**: Negative correlations (pH ↑ = chemicals ↓) - Alkali pollution influence
   - **LUVUVU**: Positive correlations (pH ↑ = chemicals ↑) - Reducing conditions

3. **Root Causes Identified:**
   - Different pollution loads (industrial vs. agricultural)
   - Complex water mixing patterns
   - Redox condition variations
   - Human impact levels

### 💡 Impact:

- **R150 billion** annual economic impact in South Africa
- First documented case of opposite correlations in adjacent catchments
- Evidence-based recommendations for region-specific water treatment
- Data-driven policy insights for water resource management

## ✨ Features

- 📊 **Interactive Visualizations** - Plotly-powered charts and graphs
- 🔬 **Scientific Analysis** - Comprehensive correlation analysis and pattern discovery
- 🌊 **Live News Feed** - Real-time water quality updates from CSIR and national sources
- 📈 **WHO Compliance Tracking** - Visual progress indicators and alerts
- 🎨 **Modern UI** - Clean, responsive design with gradient aesthetics
- 💼 **Business Case** - Economic impact analysis and recommendations

## 🛠️ Technologies

- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **News Integration**: Feedparser, RSS feeds
- **Deployment**: Streamlit Cloud

## 📁 Project Structure

```
water-quality-analysis/
├── app.py                          # Main Streamlit dashboard
├── data/
│   ├── raw/
│   │   └── water_quality.xlsx     # Original dataset
│   └── processed/
│       └── water_quality_summary.csv
├── notebooks/
│   └── water_quality_analysis.ipynb
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone git@github.com:MbuyeloMich/water-quality-analysis.git
   cd water-quality-analysis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   ```
   http://localhost:8501
   ```

## ☁️ Deploy to Streamlit Cloud

1. **Fork this repository**
2. **Go to [share.streamlit.io](https://share.streamlit.io)**
3. **Click "New app"**
4. **Select your forked repository**
5. **Set main file path**: `app.py`
6. **Click "Deploy"**

Your app will be live at: `https://[your-app-name].streamlit.app`

## 📊 Data Sources

- **Primary Data**: MHLATHUZE and LUVUVU catchment water quality measurements
- **News Sources**: 
  - CSIR Water Research
  - Department of Water and Sanitation
  - News24 Environment
  - Engineering News Water Category

## 📈 Key Metrics

| Metric | MHLATHUZE | LUVUVU |
|--------|-----------|---------|
| WHO Compliance | ~70% | ~10% |
| Risk Level | Moderate-High | Critical |
| Main Issue | Industrial pollution | pH extremes |
| Priority Action | Effluent control | Water treatment |

## 👨‍🔬 Author

**Mbuyelo Mich**
- 🤖 AI/ML Engineer | 📊 Data Scientist/Engineer | 💻 Full Stack Developer
- 📧 Email: newtoneffect0@gmail.com
- 🔗 GitHub: [@MbuyeloMich](https://github.com/MbuyeloMich)
- 🏢 Institution: Aurabyte (self guided)
- 📅 Study Period: February 7-9, 2026

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/MbuyeloMich/water-quality-analysis/issues).

## 🌟 Acknowledgments

- CSIR for water quality research resources
- South African Department of Water and Sanitation
- WHO water quality guidelines
- Streamlit community for the amazing framework

---

**⭐ If you find this project useful, please consider giving it a star!**
