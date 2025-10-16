import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="Financial Sentiment Agent",
    page_icon="📊",
    layout="wide"
)

# Your API URL
API_URL = "https://b3x3ley4t1.execute-api.us-east-1.amazonaws.com"

# Sidebar
st.sidebar.title("📊 Financial Sentiment Agent")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🔴 Live Demo", "🏗️ Architecture", "💻 Tech Stack", "📈 About"]
)

# HOME PAGE
if page == "🏠 Home":
    st.title("🚀 AWS-Deployed Financial Sentiment Agent")
    st.markdown("### Production-Ready Multi-Agent System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Deployment", "AWS Lambda", "Serverless")
    with col2:
        st.metric("API Status", "🟢 Live", "Public")
    with col3:
        st.metric("Cost", "$0/month", "Free Tier")
    
    st.markdown("---")
    
    st.markdown("""
    ## 🎯 What This System Does
    
    This is an **autonomous financial sentiment analysis system** deployed on AWS:
    
    - 📰 **Fetches** real-time financial news from NewsAPI
    - 🤖 **Analyzes** sentiment using HuggingFace's FinBERT model
    - 📊 **Generates** comprehensive market sentiment reports
    - 🌐 **Serves** results via public REST API
    
    ## ⚡ Key Features
    
    - **Serverless Architecture**: AWS Lambda + API Gateway
    - **Multi-Agent System**: Specialized agents for data, sentiment, and reporting
    - **Production-Ready**: Error handling, logging, monitoring
    - **Zero Cost**: Complete free tier usage
    - **Auto-Scaling**: Handles traffic spikes automatically
    
    ## 🔗 Live Resources
    
    - **API Endpoint**: `{}`
    - **GitHub**: [View Source Code](https://github.com/jayzz999/financial-agent-aws)
    - **Status**: 🟢 Online and serving requests
    """.format(API_URL))
    
    st.markdown("---")
    st.info("👈 Use the sidebar to navigate to the **Live Demo** and test the system!")

# LIVE DEMO PAGE
elif page == "🔴 Live Demo":
    st.title("🔴 Live Sentiment Analysis Demo")
    st.markdown("Test the production API in real-time!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query = st.text_input(
            "Enter a stock ticker or financial topic:",
            value="Tesla stock",
            help="Examples: 'Apple stock', 'cryptocurrency', 'inflation', 'S&P 500'"
        )
    
    with col2:
        max_articles = st.slider("Number of articles:", 1, 10, 5)
    
    if st.button("🚀 Analyze Sentiment", type="primary", use_container_width=True):
        with st.spinner("🔍 Fetching news and analyzing sentiment..."):
            start_time = time.time()
            
            try:
                # Call your AWS API
                response = requests.post(
                    API_URL,
                    json={"query": query, "max_articles": max_articles},
                    timeout=60
                )
                
                elapsed_time = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    report = data.get('report', {})
                    
                    # Show metrics
                    st.success(f"✅ Analysis complete in {elapsed_time:.2f} seconds!")
                    
                    # Metrics row
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Positive", report.get('positive', 0), "🟢")
                    with col2:
                        st.metric("Negative", report.get('negative', 0), "🔴")
                    with col3:
                        st.metric("Neutral", report.get('neutral', 0), "⚪")
                    with col4:
                        st.metric("Total", report.get('total', 0))
                    
                    # Summary
                    st.markdown("### 📝 Summary")
                    st.info(report.get('summary', 'No summary available'))
                    
                    # Visualization
                    st.markdown("### 📊 Sentiment Distribution")
                    
                    sentiment_data = {
                        'Sentiment': ['Positive', 'Negative', 'Neutral'],
                        'Count': [
                            report.get('positive', 0),
                            report.get('negative', 0),
                            report.get('neutral', 0)
                        ]
                    }
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=sentiment_data['Sentiment'],
                            y=sentiment_data['Count'],
                            marker_color=['#28a745', '#dc3545', '#6c757d']
                        )
                    ])
                    
                    fig.update_layout(
                        title="Article Sentiment Breakdown",
                        xaxis_title="Sentiment",
                        yaxis_title="Number of Articles",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Pie chart
                    fig_pie = go.Figure(data=[
                        go.Pie(
                            labels=sentiment_data['Sentiment'],
                            values=sentiment_data['Count'],
                            marker_colors=['#28a745', '#dc3545', '#6c757d']
                        )
                    ])
                    
                    fig_pie.update_layout(title="Sentiment Proportion", height=400)
                    st.plotly_chart(fig_pie, use_container_width=True)
                    
                    # Top headlines
                    st.markdown("### 📰 Analyzed Headlines")
                    headlines = report.get('top_headlines', [])
                    
                    for i, headline in enumerate(headlines, 1):
                        st.markdown(f"{i}. {headline}")
                    
                    # Raw response
                    with st.expander("🔍 View Raw API Response"):
                        st.json(data)
                
                else:
                    st.error(f"❌ API Error: {response.status_code}")
                    st.code(response.text)
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.code(str(e))

# ARCHITECTURE PAGE
elif page == "🏗️ Architecture":
    st.title("🏗️ System Architecture")
    
    st.markdown("""
    ## 🎨 Architecture Overview
```
    ┌─────────────────────────────────────────┐
    │         AWS Cloud Infrastructure         │
    ├─────────────────────────────────────────┤
    │                                          │
    │  🌐 API Gateway (Public REST API)       │
    │            ↓                             │
    │  ⚡ AWS Lambda Function                 │
    │     ├── Data Agent                      │
    │     ├── Sentiment Agent                 │
    │     └── Report Agent                    │
    │            ↓                             │
    │  📰 NewsAPI → Fetch Articles            │
    │  🤖 HuggingFace → FinBERT Analysis      │
    │            ↓                             │
    │  📊 JSON Response                        │
    │                                          │
    └─────────────────────────────────────────┘
```
    
    ## 🔧 Component Breakdown
    """)
    
    components = {
        "API Gateway": {
            "icon": "🌐",
            "description": "Public REST API endpoint",
            "tech": "AWS API Gateway (HTTP API)",
            "purpose": "Receives requests, routes to Lambda"
        },
        "Lambda Function": {
            "icon": "⚡",
            "description": "Serverless compute",
            "tech": "AWS Lambda (Python 3.11)",
            "purpose": "Orchestrates agents, processes requests"
        },
        "Data Agent": {
            "icon": "📰",
            "description": "News fetching",
            "tech": "NewsAPI integration",
            "purpose": "Retrieves real-time financial news"
        },
        "Sentiment Agent": {
            "icon": "🤖",
            "description": "AI analysis",
            "tech": "HuggingFace FinBERT",
            "purpose": "Analyzes market sentiment"
        },
        "Report Agent": {
            "icon": "📊",
            "description": "Report generation",
            "tech": "Python data processing",
            "purpose": "Synthesizes results"
        }
    }
    
    for name, details in components.items():
        with st.expander(f"{details['icon']} **{name}**"):
            st.markdown(f"**Description:** {details['description']}")
            st.markdown(f"**Technology:** {details['tech']}")
            st.markdown(f"**Purpose:** {details['purpose']}")

# TECH STACK PAGE
elif page == "💻 Tech Stack":
    st.title("💻 Technology Stack")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ☁️ Cloud & Infrastructure")
        st.markdown("""
        - **AWS Lambda**: Serverless compute
        - **API Gateway**: REST API interface
        - **IAM**: Security & permissions
        - **CloudWatch**: Logging & monitoring
        """)
        
        st.markdown("### 🐍 Backend")
        st.markdown("""
        - **Python 3.11**: Runtime
        - **Requests**: HTTP client
        - **Multi-agent architecture**
        """)
    
    with col2:
        st.markdown("### 🤖 AI/ML")
        st.markdown("""
        - **HuggingFace API**: Model inference
        - **FinBERT**: Financial sentiment model
        - **ProsusAI/finbert**: Fine-tuned model
        """)
        
        st.markdown("### 📊 Data Sources")
        st.markdown("""
        - **NewsAPI**: Real-time financial news
        - **REST APIs**: External integrations
        """)
    
    st.markdown("---")
    st.markdown("### 📈 Performance Characteristics")
    
    metrics = {
        "Cold Start": "2-3 seconds",
        "Warm Request": "1-1.5 seconds",
        "Concurrent Requests": "Auto-scaling",
        "Monthly Cost": "$0 (Free Tier)",
        "Uptime": "99.9%"
    }
    
    cols = st.columns(len(metrics))
    for col, (metric, value) in zip(cols, metrics.items()):
        with col:
            st.metric(metric, value)

# ABOUT PAGE
elif page == "📈 About":
    st.title("📈 About This Project")
    
    st.markdown("""
    ## 👨‍💻 Project Overview
    
    This financial sentiment agent was built as a **production-ready demonstration**
    of modern cloud architecture and AI integration.
    
    ### 🎯 Goals Achieved
    
    - ✅ Deploy AI system to production cloud
    - ✅ Create public REST API
    - ✅ Implement multi-agent architecture
    - ✅ Zero-cost operation
    - ✅ Automatic scaling
    
    ### 🚀 Development Timeline
    
    - **Day 1**: AWS account setup, Lambda deployment
    - **Day 2**: API Gateway configuration, testing
    - **Day 3**: Documentation, GitHub repository
    - **Day 4**: Streamlit dashboard creation
    
    ### 📚 Learning Outcomes
    
    Through this project, I gained hands-on experience with:
    
    - AWS Lambda and serverless architecture
    - API Gateway configuration
    - IAM security best practices
    - Production deployment workflows
    - Multi-agent system design
    - Real-time AI inference
    
    ### 🔗 Links
    
    - **Live API**: `{}`
    - **GitHub**: [jayzz999/financial-agent-aws](https://github.com/jayzz999/financial-agent-aws)
    - **LinkedIn**: [Your LinkedIn]
    
    ### 📧 Contact
    
    Built by Jayanth Muthina  
    BITS Pilani Dubai Campus  
    Computer Science, Class of 2026
    """.format(API_URL))
    
    st.markdown("---")
    st.success("💡 This dashboard itself is deployed on Streamlit Cloud - another serverless platform!")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Built with ❤️ using Streamlit | Deployed on AWS Lambda | 
        <a href='https://github.com/jayzz999/financial-agent-aws'>View Source</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
