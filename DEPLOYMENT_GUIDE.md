# 🚀 TransitIQ Enhanced - Deployment Guide

## Quick Start for Streamlit Cloud

### Step 1: Fork the Repository
1. Go to https://github.com/WalkerVVV/TransitIQ-Enhanced
2. Click the "Fork" button in the top right
3. This creates your own copy of the repository

### Step 2: Deploy on Streamlit Cloud
1. Visit https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in:
   - **Repository**: `YourGitHubUsername/TransitIQ-Enhanced`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click "Deploy!"

### Step 3: Wait for Deployment
- First deployment takes 2-5 minutes
- You'll see build logs in real-time
- Once complete, you'll get a URL like: `https://transitiq-enhanced.streamlit.app`

## 🔧 Troubleshooting Deployment Issues

### Issue: "Module not found" errors
**Solution**: The requirements.txt file includes all dependencies. If issues persist:
```bash
# Update requirements.txt with:
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
xlsxwriter==3.1.9
openpyxl==3.1.2
```

### Issue: "Resource limits exceeded"
**Solution**: Streamlit Cloud free tier limits:
- 1GB RAM
- 1GB storage

Optimize by:
1. Limiting data to last 90 days
2. Reducing demo data size
3. Using data sampling for large files

### Issue: "App not loading / blank screen"
**Solution**: Check browser console for errors:
1. Press F12 in browser
2. Go to Console tab
3. Look for red error messages
4. Common fix: Clear browser cache

## 📊 Verifying All 11 Sections

### Without Data Upload
1. Open your deployed app
2. In sidebar, select "Demo Data Type" → "Complete Dataset"
3. All 11 sections should display with sample data

### With Your Data
1. Prepare CSV/Excel with columns:
   - Xparcel Type (Ground/Expedited/Priority)
   - Days In Transit
   - Calculated Zone (1-8)
   - Destination State
   - Weight
   - Cost
2. Upload file in sidebar
3. Enable "Debug Mode" to see processing details

## 🎯 Section Visibility Checklist

| # | Section | Always Visible? | Required Data |
|---|---------|----------------|----------------|
| 1 | Executive Summary | ✅ Yes | None (uses defaults) |
| 2 | Performance by Xparcel Tier | ✅ Yes | Xparcel Type, Days In Transit |
| 3 | Service Mix | ✅ Yes | Xparcel Type |
| 4 | Zone Distribution | ✅ Yes | Calculated Zone |
| 5 | Exception Summary | ✅ Yes | SLA Status (auto-calculated) |
| 6 | Regional Performance | ✅ Yes | Destination State |
| 7 | Day-of-Week | ✅ Yes | Request Date |
| 8 | Weight Impact | ✅ Yes | Weight |
| 9 | Carrier Performance | ✅ Yes | Carrier (or uses demo) |
| 10 | Cost Analysis | ✅ Yes | Cost |
| 11 | Routing Recommendations | ✅ Yes | None (uses analysis) |

## 🛠️ Advanced Configuration

### Custom Domain
1. In Streamlit Cloud settings
2. Add custom domain
3. Follow CNAME instructions

### Environment Variables
```python
# In Streamlit Cloud settings, add:
DEBUG_MODE=true
MAX_UPLOAD_SIZE=200
DEFAULT_DEMO_TYPE=Complete Dataset
```

### Performance Optimization
```python
# Add to app.py for caching:
@st.cache_data
def load_data(file):
    # Data loading logic
    return df

@st.cache_resource
def init_toolkits():
    # Initialize heavy resources
    return toolkits
```

## 📱 Mobile Optimization

The dashboard is responsive but for best mobile experience:
1. Use landscape orientation
2. Zoom out to 80% for full view
3. Use collapsible sections

## 🔐 Security & Privacy

### Data Handling
- All processing happens in-browser
- No data is stored on servers
- Uploads are temporary (session only)

### Access Control
1. Make repository private if needed
2. Streamlit Cloud respects GitHub permissions
3. Use Streamlit's built-in authentication

## 📧 Support

### Getting Help
1. **Debug Mode**: Enable in sidebar for diagnostics
2. **GitHub Issues**: https://github.com/WalkerVVV/TransitIQ-Enhanced/issues
3. **Streamlit Forums**: https://discuss.streamlit.io

### Common Questions

**Q: Why do some sections show "No data available"?**
A: Enable demo data or ensure your upload has required columns.

**Q: Can I customize the carrier list?**
A: Yes! Edit `SELECT_CARRIERS` in dashboard.py

**Q: How do I export all 11 sections?**
A: Use the Excel export button - it includes all sections as separate sheets.

---

**FirstMile | Shipping Without Limits**
