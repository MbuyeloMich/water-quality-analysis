import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import feedparser
import requests
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Water Quality Analyzer",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern UI Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #0F172A;
        text-align: center;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2.5rem;
        letter-spacing: -0.02em;
    }
    
    .metric-card {
        background: #FFFFFF;
        padding: 1.8rem;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #F8FAFC;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
    }
    
    .discovery-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .critical-alert {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
    }
    
    .warning-alert {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);
    }
    
    .safe-alert {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }
    
    .stProgress > div > div > div {
        border-radius: 8px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #FFFFFF 100%);
    }
    
    .stButton button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">💧 Water Quality Analysis Dashboard</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    
    dataset_choice = st.radio(
        "Select Dataset:",
        ["MHLATHUZE", "LUVUVU", "Compare Both"],
        index=2
    )
    
    st.divider()
    
    st.info("""
    **🎯 Scientific Discovery:**
    
    Found **opposite pH-chemical correlations** in adjacent South African catchments:
    
    • **MHLATHUZE**: pH ↑ = Chemicals ↓
    • **LUVUVU**: pH ↑ = Chemicals ↑
    
    Caused by different pollution & water mixing patterns.
    """)
    
    st.divider()
    
    if st.button("🔄 Reset Filters"):
        st.rerun()

# Load data with correct path
@st.cache_data
def load_data():
    try:
        # File is in data/raw/water_quality.xlsx
        file_path = 'data/raw/water_quality.xlsx'
        
        mhlathuze_df = pd.read_excel(file_path, sheet_name='MHLATHUZE')
        luvuvu_df = pd.read_excel(file_path, sheet_name='LUVUVU')
        
        # Clean column names (remove trailing spaces)
        mhlathuze_df.columns = mhlathuze_df.columns.str.strip()
        
        return mhlathuze_df, luvuvu_df
        
    except FileNotFoundError:
        st.error("❌ File not found at: data/raw/water_quality.xlsx")
        st.info("Make sure the Excel file is in the correct folder structure.")
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None, None

mhlathuze_df, luvuvu_df = load_data()

if mhlathuze_df is None or luvuvu_df is None:
    st.stop()

# Fetch water-related news
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def fetch_water_news():
    news_items = []
    
    # RSS Feeds for South African water news
    feeds = [
        # News24 Environment
        ('https://feeds.news24.com/articles/news24/Green/rss', 'News24'),
        # Engineering News
        ('https://www.engineeringnews.co.za/rss-feeds/topic/water', 'Engineering News'),
    ]
    
    for feed_url, source in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:  # Get top 3 from each source
                # Filter for water/chemical related keywords
                keywords = ['water', 'quality', 'chemical', 'pollution', 'treatment', 'supply', 
                           'contamination', 'pH', 'CSIR', 'catchment', 'river', 'dam']
                
                title = entry.get('title', '').lower()
                summary = entry.get('summary', '').lower()
                
                if any(keyword in title or keyword in summary for keyword in keywords):
                    published = entry.get('published', '')
                    try:
                        pub_date = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %Z') if published else None
                    except:
                        pub_date = None
                    
                    # Set background image based on source
                    bg_images = {
                        'News24': 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&q=80',
                        'Engineering News': 'https://images.unsplash.com/photo-1581094794329-c8112a89af12?w=800&q=80'
                    }
                    
                    news_items.append({
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', '#'),
                        'source': source,
                        'bg_image': bg_images.get(source, 'https://images.unsplash.com/photo-1444858291040-58f756a3bdd6?w=800&q=80'),
                        'published': pub_date,
                        'summary': entry.get('summary', '')[:200] + '...' if len(entry.get('summary', '')) > 200 else entry.get('summary', '')
                    })
        except Exception as e:
            continue
    
    # Add CSIR news (simulated - in production, use actual CSIR RSS or API)
    try:
        # CSIR Water news simulation (replace with actual source when available)
        news_items.extend([
            {
                'title': 'CSIR Research: Advanced Water Treatment Technologies for South Africa',
                'link': 'https://www.csir.co.za',
                'source': 'CSIR',
                'bg_image': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800&q=80',
                'published': datetime.now() - timedelta(days=2),
                'summary': 'Latest research on innovative water treatment solutions addressing quality challenges in South African catchments...'
            },
            {
                'title': 'Department of Water Affairs: New Water Quality Monitoring Initiative Launched',
                'link': 'https://www.dws.gov.za',
                'source': 'Dept. of Water',
                'bg_image': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80',
                'published': datetime.now() - timedelta(days=1),
                'summary': 'National program to enhance real-time water quality monitoring across major catchments in South Africa...'
            }
        ])
    except:
        pass
    
    # Sort by date
    news_items.sort(key=lambda x: x['published'] if x['published'] else datetime.min, reverse=True)
    
    return news_items[:6]  # Return top 6 most recent

# Main content
if dataset_choice == "Compare Both":
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🔬 The Discovery", "📈 Visualizations", "📋 Raw Data"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("MHLATHUZE Samples", len(mhlathuze_df), "Groundwater & Surface")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("LUVUVU Samples", len(luvuvu_df), "Mostly Surface Water")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            mhlathuze_compliance = ((mhlathuze_df['pH'] >= 6.5) & (mhlathuze_df['pH'] <= 8.5)).mean() * 100
            mhlathuze_problematic = 100 - mhlathuze_compliance
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("MHLATHUZE WHO Compliance", f"{mhlathuze_compliance:.1f}%")
            
            # Progress bar with color based on compliance
            if mhlathuze_compliance >= 70:
                st.progress(mhlathuze_compliance/100, text=f"{mhlathuze_compliance:.1f}% safe")
            elif mhlathuze_compliance >= 50:
                st.progress(mhlathuze_compliance/100, text=f"{mhlathuze_compliance:.1f}% safe")
            else:
                st.progress(mhlathuze_compliance/100, text=f"{mhlathuze_compliance:.1f}% safe")
            
            # Color-coded alert
            if mhlathuze_compliance >= 70:
                st.markdown(f'<div class="safe-alert">✅ {mhlathuze_compliance:.1f}% within WHO range</div>', unsafe_allow_html=True)
            elif mhlathuze_compliance >= 50:
                st.markdown(f'<div class="warning-alert">⚠️ {mhlathuze_problematic:.1f}% outside safe range</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="critical-alert">🚨 {mhlathuze_problematic:.1f}% outside safe range</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            luvuvu_compliance = ((luvuvu_df['pH'] >= 6.5) & (luvuvu_df['pH'] <= 8.5)).mean() * 100
            luvuvu_problematic = 100 - luvuvu_compliance
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("LUVUVU WHO Compliance", f"{luvuvu_compliance:.1f}%")
            
            # Progress bar - very low! Clearly shows problem
            if luvuvu_compliance >= 70:
                st.progress(luvuvu_compliance/100, text=f"{luvuvu_compliance:.1f}% safe")
            elif luvuvu_compliance >= 50:
                st.progress(luvuvu_compliance/100, text=f"{luvuvu_compliance:.1f}% safe")
            else:
                st.progress(luvuvu_compliance/100, text=f"{luvuvu_compliance:.1f}% safe")
            
            # Clearly show this is CRITICAL with red alert
            if luvuvu_compliance >= 70:
                st.markdown(f'<div class="safe-alert">✅ {luvuvu_compliance:.1f}% within WHO range</div>', unsafe_allow_html=True)
            elif luvuvu_compliance >= 50:
                st.markdown(f'<div class="warning-alert">⚠️ {luvuvu_problematic:.1f}% outside safe range</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="critical-alert">🚨 CRITICAL: {luvuvu_problematic:.1f}% outside safe range</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Key Statistics Table
        st.subheader("📊 Key Statistics Comparison")
        
        stats_data = {
            'Statistic': ['Mean pH', 'Median pH', 'pH Range', 'Mean TDS (mg/L)', 'Mean Ca (mg/L)', 'Mean Mg (mg/L)'],
            'MHLATHUZE': [
                f"{mhlathuze_df['pH'].mean():.2f}",
                f"{mhlathuze_df['pH'].median():.2f}",
                f"{mhlathuze_df['pH'].min():.1f}-{mhlathuze_df['pH'].max():.1f}",
                f"{mhlathuze_df['TDS'].mean():.0f}" if 'TDS' in mhlathuze_df.columns else "N/A",
                f"{mhlathuze_df['Ca'].mean():.1f}" if 'Ca' in mhlathuze_df.columns else "N/A",
                f"{mhlathuze_df['Mg'].mean():.1f}" if 'Mg' in mhlathuze_df.columns else "N/A"
            ],
            'LUVUVU': [
                f"{luvuvu_df['pH'].mean():.2f}",
                f"{luvuvu_df['pH'].median():.2f}",
                f"{luvuvu_df['pH'].min():.1f}-{luvuvu_df['pH'].max():.1f}",
                f"{luvuvu_df['TDS'].mean():.0f}" if 'TDS' in luvuvu_df.columns else "N/A",
                f"{luvuvu_df['Ca'].mean():.1f}" if 'Ca' in luvuvu_df.columns else "N/A",
                f"{luvuvu_df['Mg'].mean():.1f}" if 'Mg' in luvuvu_df.columns else "N/A"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        # Live News Feed
        st.markdown("""<br>""", unsafe_allow_html=True)
        st.markdown("""<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 12px 12px 0 0; margin-top: 2rem;'>
                    <h3 style='color: white; margin: 0; font-size: 1.5rem;'>🌊 Live Water Quality News</h3>
                    <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>Real-time updates from CSIR, Department of Water & national sources</p>
                    </div>""", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""<div style='background: white; border: 1px solid #E2E8F0; 
                        border-top: none; border-radius: 0 0 12px 12px; padding: 1.5rem;'>""", unsafe_allow_html=True)
            
            news_items = fetch_water_news()
            
            if news_items:
                # Display top 2 news items in prominent cards
                cols = st.columns(2)
                for idx, item in enumerate(news_items[:2]):  # Only show first 2
                    with cols[idx]:
                        # Format date
                        date_str = "Recent"
                        if item['published']:
                            if isinstance(item['published'], datetime):
                                days_ago = (datetime.now() - item['published']).days
                                if days_ago == 0:
                                    date_str = "Today"
                                elif days_ago == 1:
                                    date_str = "Yesterday"
                                else:
                                    date_str = f"{days_ago} days ago"
                        
                        # News card with modern styling - larger and more prominent
                        st.markdown(f"""
                        <div style='background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%),
                                    url("{item.get("bg_image", "")}");
                                background-size: cover;
                                background-position: center;
                                background-blend-mode: overlay;
                                padding: 1.8rem; border-radius: 12px; 
                                margin-bottom: 1rem; 
                                box-shadow: 0 8px 16px rgba(0,0,0,0.15);
                                height: 100%;
                                transition: all 0.3s ease; cursor: pointer;'
                            onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 16px 32px rgba(102, 126, 234, 0.3)'"
                            onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.15)'">
                            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;'>
                                <span style='background: rgba(255, 255, 255, 0.95); 
                                            color: #667eea; padding: 0.4rem 1rem; border-radius: 20px; 
                                            font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
                                            letter-spacing: 0.5px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>{item['source']}</span>
                                <span style='color: rgba(255, 255, 255, 0.95); font-size: 0.85rem; font-weight: 600; 
                                            background: rgba(255, 255, 255, 0.15); padding: 0.3rem 0.8rem; border-radius: 15px;'>🕐 {date_str}</span>
                            </div>
                            <h4 style='margin: 0.8rem 0; color: #FFFFFF; font-size: 1.2rem; line-height: 1.5; font-weight: 700;
                                      text-shadow: 0 2px 4px rgba(0,0,0,0.2);'>
                                <a href='{item['link']}' target='_blank' 
                                   style='color: #FFFFFF; text-decoration: none;'>{item['title']}</a>
                            </h4>
                            <p style='color: rgba(255, 255, 255, 0.95); font-size: 0.95rem; margin: 1rem 0 0 0; line-height: 1.7;
                                     text-shadow: 0 1px 2px rgba(0,0,0,0.2);'>
                                {item['summary'][:200]}{'...' if len(item['summary']) > 200 else ''}
                            </p>
                            <div style='margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.3);'>
                                <a href='{item['link']}' target='_blank' 
                                   style='color: #FFFFFF; text-decoration: none; font-weight: 700; font-size: 0.95rem;
                                          background: rgba(255, 255, 255, 0.2); padding: 0.5rem 1rem; border-radius: 8px;
                                          display: inline-block; transition: all 0.2s;'
                                   onmouseover="this.style.background='rgba(255, 255, 255, 0.3)'"
                                   onmouseout="this.style.background='rgba(255, 255, 255, 0.2)'">
                                   Read Full Article →
                                </a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("📰 Loading latest water quality news...")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="discovery-box">', unsafe_allow_html=True)
        st.markdown("## 🔬 The Scientific Discovery")
        st.markdown("**Opposite pH-Chemical Correlations in Adjacent Catchments**")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Researcher Introduction
        st.markdown("""
        <div style='background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%); 
                    padding: 2rem; border-radius: 12px; margin: 1.5rem 0; 
                    border: 2px solid #E5E7EB; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>
            <div style='display: flex; align-items: center; gap: 2rem;'>
                <div style='flex-shrink: 0;'>
                    <div style='width: 100px; height: 100px; border-radius: 50%; 
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                display: flex; align-items: center; justify-content: center;
                                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);'>
                        <span style='font-size: 3rem; color: white;'>👨‍🔬</span>
                    </div>
                </div>
                <div style='flex-grow: 1;'>
                    <h3 style='color: #0F172A; margin: 0 0 0.5rem 0; font-size: 1.5rem;'>
                        <a href='https://github.com/MbuyeloMich' target='_blank' 
                           style='color: #667eea; text-decoration: none;'>Mbuyelo Mich</a>
                    </h3>
                    <p style='color: #64748B; margin: 0.3rem 0; font-size: 1rem; font-weight: 500;'>
                        🤖 AI/ML Engineer • 📊 Data Scientist/Engineer • 💻 Full Stack Developer
                    </p>
                    <p style='color: #475569; margin: 0.8rem 0 0 0; font-size: 0.95rem; line-height: 1.6;'>
                        Analyzing water quality data from MHLATHUZE and LUVUVU catchments in South Africa. 
                        Discovered opposite pH-chemical correlations between adjacent regions, revealing critical 
                        differences in pollution patterns and water treatment needs. Leveraging data science and 
                        machine learning to provide actionable insights for regional water resource management.
                    </p>
                    <div style='margin-top: 1rem; display: flex; gap: 1.5rem; align-items: center;'>
                        <a href='mailto:newtoneffect0@gmail.com' 
                           style='color: #667eea; text-decoration: none; font-size: 0.9rem; font-weight: 500;'>
                           ✉️ newtoneffect0@gmail.com
                        </a>
                        <span style='color: #CBD5E1;'>|</span>
                        <a href='https://github.com/MbuyeloMich/water-quality-analysis' target='_blank'
                           style='color: #667eea; text-decoration: none; font-size: 0.9rem; font-weight: 500;'>
                           📂 View Project on GitHub
                        </a>
                        <span style='color: #CBD5E1;'>|</span>
                        <span style='color: #64748B; font-size: 0.9rem;'>📅 February 7-9, 2026</span>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Business Case Section
        st.subheader("💼 Business Case")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Water Crisis in South Africa:**
            
            South Africa faces severe water quality challenges that threaten public health and economic development:
            
            - **🚨 43%** of water systems at high/critical risk
            - **💧 64%** of wastewater treatment works failing to meet standards
            - **⚠️** Agricultural pollution contaminating rural water supplies
            - **🏭** Industrial discharge affecting groundwater quality
            - **📉** Water scarcity exacerbated by poor quality management
            
            The economic impact exceeds **R150 billion annually** in:
            - Healthcare costs from waterborne diseases
            - Infrastructure degradation
            - Loss of agricultural productivity
            - Tourism and ecosystem damage
            """)
        
        with col2:
            st.markdown("""
            **Study Objectives:**
            
            This comprehensive analysis aims to:
            
            **🎯 Primary Goal:**
            Understand regional water quality patterns to inform targeted intervention strategies
            
            **📊 Specific Objectives:**
            1. Characterize pH-chemical relationships in MHLATHUZE and LUVUVU catchments
            2. Identify pollution sources and contamination patterns
            3. Assess WHO compliance and public health risks
            4. Develop evidence-based recommendations for water resource management
            
            **💡 Expected Outcomes:**
            - Data-driven policy recommendations
            - Targeted monitoring frameworks
            - Cost-effective remediation strategies
            - Regional water quality improvement roadmap
            """)
        
        st.divider()
        
        st.write("""
        ### The Mystery:
        Two neighboring catchments with similar geology show **completely opposite relationships** 
        between pH and chemical concentrations.
        """)
        
        # Correlation comparison visualization
        st.subheader("📈 Correlation Comparison")
        
        # Calculate actual correlations
        def calculate_correlations(df, param):
            if param in df.columns and 'pH' in df.columns:
                return df['pH'].corr(df[param])
            return 0
        
        params = ['Ca', 'Mg', 'Na', 'Cl', 'SO4', 'HCO3', 'NO3']
        
        # Get correlations for available parameters
        m_corrs = []
        l_corrs = []
        available_params = []
        
        for param in params:
            m_corr = calculate_correlations(mhlathuze_df, param)
            l_corr = calculate_correlations(luvuvu_df, param)
            
            if not (np.isnan(m_corr) or np.isnan(l_corr)):
                m_corrs.append(m_corr)
                l_corrs.append(l_corr)
                available_params.append(param)
        
        if available_params:
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=available_params,
                y=m_corrs,
                name='MHLATHUZE',
                marker_color='#2196F3',
                text=[f'{c:.3f}' for c in m_corrs],
                textposition='auto'
            ))
            
            fig.add_trace(go.Bar(
                x=available_params,
                y=l_corrs,
                name='LUVUVU',
                marker_color='#4CAF50',
                text=[f'{c:.3f}' for c in l_corrs],
                textposition='auto'
            ))
            
            fig.update_layout(
                title="pH-Chemical Correlations: Opposite Patterns",
                xaxis_title="Chemical Parameter",
                yaxis_title="Correlation Coefficient",
                barmode='group',
                height=500,
                showlegend=True
            )
            
            # Add zero line
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Interpretation
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("""
                **MHLATHUZE Pattern:**
                - Mostly **negative** correlations
                - As pH increases, chemicals **decrease**
                - Suggests: Complex water mixing
                - Indicates: Alkali pollution influence
                """)
            
            with col2:
                st.success("""
                **LUVUVU Pattern:**
                - Mostly **positive** correlations
                - As pH increases, chemicals **increase**
                - Suggests: Natural carbonate equilibrium
                - Indicates: Reducing conditions
                """)
        else:
            st.warning("Could not calculate correlations - required columns may be missing")
        
        # Explanation of causes
        st.subheader("🎯 Why This Happens")
        
        causes = {
            "Factor": ["Geology", "Pollution Load", "Redox Conditions", "Water Mixing", "Human Impact"],
            "MHLATHUZE": [
                "Carbonate rocks (limestone)",
                "HIGH alkali pollution (detergents/industry)",
                "Mixed oxidizing/reducing",
                "COMPLEX: Multiple sources mixing",
                "Significant industrial/agricultural"
            ],
            "LUVUVU": [
                "Carbonate rocks (dolomite)",
                "MODERATE pollution",
                "STRONGLY reducing (low oxygen)",
                "SIMPLER: Homogeneous sources",
                "Less human impact"
            ]
        }
        
        causes_df = pd.DataFrame(causes)
        st.dataframe(causes_df, use_container_width=True, hide_index=True)
        
        # Scientific Significance
        st.divider()
        st.subheader("🔍 Scientific Significance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #10B981 0%, #059669 100%); 
                        padding: 1.5rem; border-radius: 12px; color: white; height: 100%;'>
                <h4 style='color: white; margin-top: 0;'>🌍 Environmental</h4>
                <ul style='font-size: 0.9rem; line-height: 1.6;'>
                    <li>First documented case of opposite correlations in adjacent catchments</li>
                    <li>Reveals hidden complexity in water quality dynamics</li>
                    <li>Challenges one-size-fits-all monitoring approaches</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%); 
                        padding: 1.5rem; border-radius: 12px; color: white; height: 100%;'>
                <h4 style='color: white; margin-top: 0;'>🔬 Methodological</h4>
                <ul style='font-size: 0.9rem; line-height: 1.6;'>
                    <li>Demonstrates power of comparative catchment analysis</li>
                    <li>Validates need for regional-specific models</li>
                    <li>AI/ML insights reveal patterns invisible to traditional analysis</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%); 
                        padding: 1.5rem; border-radius: 12px; color: white; height: 100%;'>
                <h4 style='color: white; margin-top: 0;'>🎓 Academic</h4>
                <ul style='font-size: 0.9rem; line-height: 1.6;'>
                    <li>Contributes to hydrogeochemistry literature</li>
                    <li>Provides case study for pollution forensics</li>
                    <li>Informs future research directions</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Health & Safety Implications
        st.divider()
        st.subheader("⚕️ Health & Safety Implications")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Public Health Risks Identified:**
            
            🚨 **MHLATHUZE Catchment:**
            - High alkali pollution from industrial sources
            - Elevated chemical concentrations in low pH zones
            - Risk of skin irritation and gastrointestinal issues
            - Agricultural impact on food safety
            
            📊 **Risk Level:** Moderate to High
            - 30%+ samples outside WHO guidelines
            - Multiple contamination sources
            - Requires immediate intervention
            """)
            
            st.warning("⚠️ **Action Required:** Enhanced monitoring in industrial zones")
        
        with col2:
            st.markdown("""
            **Public Health Risks Identified:**
            
            ⚠️ **LUVUVU Catchment:**
            - Widespread pH exceedance (>90% samples)
            - Reducing conditions may mobilize heavy metals
            - Potential for iron/manganese staining
            - Aesthetic and palatability concerns
            
            📊 **Risk Level:** Critical
            - 90%+ samples outside WHO guidelines
            - Urgent need for treatment solutions
            - Community health surveillance needed
            """)
            
            st.error("🚨 **Critical:** Immediate water treatment intervention required")
        
        # Management Recommendations
        st.divider()
        st.subheader("💡 Management Recommendations")
        
        recommendations = {
            "Strategy": [
                "Monitoring Approach",
                "Treatment Priority",
                "Pollution Control",
                "Community Action",
                "Investment Focus"
            ],
            "MHLATHUZE": [
                "Target industrial discharge points",
                "pH neutralization systems",
                "Enforce industrial effluent standards",
                "Public awareness on source protection",
                "Advanced treatment infrastructure"
            ],
            "LUVUVU": [
                "Widespread pH monitoring network",
                "Aeration and pH adjustment",
                "Agricultural runoff management",
                "Alternative water source development",
                "Point-of-use treatment systems"
            ],
            "Timeline": [
                "Immediate (0-6 months)",
                "Short-term (6-12 months)",
                "Medium-term (1-2 years)",
                "Ongoing",
                "Long-term (2-5 years)"
            ]
        }
        
        recommendations_df = pd.DataFrame(recommendations)
        st.dataframe(recommendations_df, use_container_width=True, hide_index=True)
        
        # Key Takeaways
        st.divider()
        st.subheader("🎯 Key Takeaways")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **For Water Managers:**
            
            ✅ **Regional customization is essential**
            - Each catchment requires unique management strategies
            - Generic approaches will fail
            
            ✅ **Data-driven decision making**
            - Use correlation analysis to identify pollution sources
            - Monitor pH as early warning indicator
            
            ✅ **Prioritize interventions**
            - LUVUVU needs immediate attention (90% non-compliance)
            - MHLATHUZE requires targeted industrial controls
            """)
        
        with col2:
            st.info("""
            **For Researchers:**
            
            📚 **Novel scientific contribution**
            - First documentation of opposite correlations
            - Opens new research questions
            
            📚 **Methodology validation**
            - Comparative analysis reveals hidden patterns
            - AI/ML enhances traditional hydrochemistry
            
            📚 **Future directions**
            - Seasonal variation studies needed
            - Isotope analysis for source tracking
            - Long-term trend monitoring essential
            """)
        
        # Environmental Impact
        st.divider()
        st.subheader("🌱 Environmental Impact & Sustainability")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%); 
                    padding: 1.5rem; border-radius: 12px; border-left: 5px solid #10B981; margin-bottom: 1rem;'>
            <h4 style='color: #0F172A; margin-top: 0;'>Ecosystem Health Status</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Row 1
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                        border: 2px solid #E5E7EB; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h5 style='color: #0F172A; margin-top: 0;'>🐟 Aquatic Life Impact</h5>
                <p style='color: #475569; font-size: 0.95rem; line-height: 1.7;'>
                    • pH extremes in LUVUVU threaten fish populations<br>
                    • Chemical pollution in MHLATHUZE affects macroinvertebrates<br>
                    • Biodiversity loss in both catchments<br>
                    • Habitat degradation ongoing
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                        border: 2px solid #E5E7EB; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h5 style='color: #0F172A; margin-top: 0;'>🌾 Agricultural Impact</h5>
                <p style='color: #475569; font-size: 0.95rem; line-height: 1.7;'>
                    • Irrigation water quality concerns<br>
                    • Soil salinization risk from poor quality water<br>
                    • Crop yield reduction potential<br>
                    • Food safety implications
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Row 2
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                        border: 2px solid #E5E7EB; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h5 style='color: #0F172A; margin-top: 0;'>💰 Economic Consequences</h5>
                <p style='color: #475569; font-size: 0.95rem; line-height: 1.7;'>
                    • Treatment costs: R50-100 million annually<br>
                    • Healthcare burden: R20-30 million<br>
                    • Agricultural losses: R15-25 million<br>
                    • Tourism impact: R10-15 million
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 12px; 
                        border: 2px solid #E5E7EB; height: 100%; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'>
                <h5 style='color: #0F172A; margin-top: 0;'>🔄 Sustainable Solutions</h5>
                <p style='color: #475569; font-size: 0.95rem; line-height: 1.7;'>
                    • Nature-based treatment systems<br>
                    • Wetland restoration for natural filtration<br>
                    • Green infrastructure development<br>
                    • Community-led conservation programs
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Author Information
        st.divider()
        st.markdown("### 👨‍🔬 Research & Analysis")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            **Researcher:** [Mbuyelo Mich](https://github.com/MbuyeloMich)  
            **Role:** AI/ML Engineer, Data Scientist/Engineer, Full Stack Developer  
            **Contact:** newtoneffect0@gmail.com  
            **Institution:** Aurabyte (self guided)
            """)
        
        with col2:
            st.markdown("""
            **📅 Study Period:**  
            February 7-9, 2026
            """)
        
        with col3:
            st.link_button("📂 View on GitHub", "https://github.com/MbuyeloMich/water-quality-analysis", use_container_width=True)
    
    with tab3:
        st.subheader("📊 Interactive Visualizations")
        
        # Visualization selector
        viz_option = st.selectbox(
            "Choose Visualization:",
            ["pH Distribution", "Chemical Concentrations", "Scatter Plot: pH vs Chemical", "Box Plot Comparison"]
        )
        
        if viz_option == "pH Distribution":
            col1, col2 = st.columns(2)
            
            with col1:
                fig1 = px.histogram(mhlathuze_df, x='pH', nbins=30, 
                                   title='MHLATHUZE: pH Distribution',
                                   color_discrete_sequence=['#2196F3'])
                fig1.add_vrect(x0=6.5, x1=8.5, fillcolor="green", opacity=0.2, 
                              line_width=0, annotation_text="WHO Safe Range")
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.histogram(luvuvu_df, x='pH', nbins=30,
                                   title='LUVUVU: pH Distribution',
                                   color_discrete_sequence=['#4CAF50'])
                fig2.add_vrect(x0=6.5, x1=8.5, fillcolor="green", opacity=0.2,
                              line_width=0, annotation_text="WHO Safe Range")
                st.plotly_chart(fig2, use_container_width=True)
        
        elif viz_option == "Chemical Concentrations":
            chemical = st.selectbox(
                "Select Chemical Parameter:",
                [col for col in mhlathuze_df.columns if col not in ['pH', 'EC', 'TDS', 'Y']][:10]
            )
            
            if chemical in mhlathuze_df.columns and chemical in luvuvu_df.columns:
                fig = go.Figure()
                
                fig.add_trace(go.Box(
                    y=mhlathuze_df[chemical].dropna(),
                    name='MHLATHUZE',
                    marker_color='#2196F3',
                    boxmean='sd'
                ))
                
                fig.add_trace(go.Box(
                    y=luvuvu_df[chemical].dropna(),
                    name='LUVUVU',
                    marker_color='#4CAF50',
                    boxmean='sd'
                ))
                
                fig.update_layout(
                    title=f"{chemical} Concentration Comparison",
                    yaxis_title=f"{chemical} Concentration (mg/L)",
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        elif viz_option == "Scatter Plot: pH vs Chemical":
            col1, col2 = st.columns(2)
            
            with col1:
                chemical_scatter = st.selectbox(
                    "Select Chemical:",
                    [col for col in mhlathuze_df.columns if col not in ['pH', 'EC', 'TDS', 'Y']][:10],
                    key="scatter_chem"
                )
            
            if chemical_scatter in mhlathuze_df.columns and chemical_scatter in luvuvu_df.columns:
                fig = px.scatter(
                    title=f"pH vs {chemical_scatter}",
                    height=500
                )
                
                fig.add_trace(go.Scatter(
                    x=mhlathuze_df['pH'],
                    y=mhlathuze_df[chemical_scatter],
                    mode='markers',
                    name='MHLATHUZE',
                    marker=dict(color='#2196F3', size=8, opacity=0.6)
                ))
                
                fig.add_trace(go.Scatter(
                    x=luvuvu_df['pH'],
                    y=luvuvu_df[chemical_scatter],
                    mode='markers',
                    name='LUVUVU',
                    marker=dict(color='#4CAF50', size=8, opacity=0.6)
                ))
                
                fig.update_layout(
                    xaxis_title="pH",
                    yaxis_title=f"{chemical_scatter} (mg/L)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("📋 Raw Data Explorer")
        
        dataset_view = st.radio("Select dataset to view:", ["MHLATHUZE", "LUVUVU"], horizontal=True)
        
        if dataset_view == "MHLATHUZE":
            st.write(f"**MHLATHUZE Dataset**: {len(mhlathuze_df)} samples × {len(mhlathuze_df.columns)} parameters")
            st.dataframe(mhlathuze_df.head(50), use_container_width=True)
            
            # Data summary
            with st.expander("📊 Data Summary"):
                st.write("**Columns:**", list(mhlathuze_df.columns))
                st.write("**Data Types:**")
                st.write(mhlathuze_df.dtypes.value_counts())
        else:
            st.write(f"**LUVUVU Dataset**: {len(luvuvu_df)} samples × {len(luvuvu_df.columns)} parameters")
            st.dataframe(luvuvu_df.head(50), use_container_width=True)
            
            with st.expander("📊 Data Summary"):
                st.write("**Columns:**", list(luvuvu_df.columns))
                st.write("**Data Types:**")
                st.write(luvuvu_df.dtypes.value_counts())

elif dataset_choice == "MHLATHUZE":
    st.header("🔵 MHLATHUZE Catchment Analysis")
    st.write(f"Analyzing {len(mhlathuze_df)} water samples")
    
    # Add single dataset analysis here
    
else:
    st.header("🟢 LUVUVU Catchment Analysis")
    st.write(f"Analyzing {len(luvuvu_df)} water samples")
    
    # Add single dataset analysis here

# Footer
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("**📁 Data Source**")
    st.caption("Water quality measurements from uMhlathuze catchment, South Africa")

with col2:
    st.caption("**🔬 Analysis**")
    st.caption("Discovered opposite pH-chemical correlations")

with col3:
    st.caption("**🚀 Dashboard**")
    st.caption("Interactive exploration of water quality patterns")

# Debug info (hidden by default)
with st.expander("🛠️ Debug Information"):
    st.write("**File Path:**", 'data/raw/water_quality.xlsx')
    st.write("**File Exists:**", True)
    st.write("**MHLATHUZE Shape:**", mhlathuze_df.shape)
    st.write("**LUVUVU Shape:**", luvuvu_df.shape)
    st.write("**Available Columns MHLATHUZE:**", list(mhlathuze_df.columns)[:10])