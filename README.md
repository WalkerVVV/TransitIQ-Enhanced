# FirstMile TransitIQ Enhanced - Shipping Analytics Dashboard

## 🎆 New: FirstMile Clean Design!

### What's New
- **FirstMile Brand Colors**: Green (#5CB85C) and Navy (#1E3A8A)
- **No Matplotlib Required**: Removed all gradient dependencies
- **Clean Modern Design**: Card-based layout matching FirstMile.com
- **Professional Tables**: 14px font with proper 12px padding
- **Performance Indicators**: Solid colors (Green/Yellow/Red)
- **Fixed Configuration Errors**: Resolved duplicate st.set_page_config

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/WalkerVVV/TransitIQ-Enhanced.git
cd TransitIQ-Enhanced

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

Or simply double-click: `run_firstmile_dashboard.bat`

## 🎯 Features

### 11 Dashboard Sections
1. **Executive Summary** - Key metrics at a glance
2. **Performance by Xparcel Tier** - Priority/Expedited/Ground analysis
3. **Service Mix Analysis** - Service distribution insights
4. **Zone Distribution & Transit** - Geographic performance
5. **Exception Summary & Hotspots** - Problem area identification
6. **Regional Performance** - State-by-state analysis
7. **Day-of-Week Performance** - Daily pattern analysis
8. **Weight Impact Analysis** - Weight-based performance
9. **Carrier Performance Scorecard** - Carrier comparisons
10. **Cost Optimization Analysis** - Savings opportunities
11. **Strategic Routing Recommendations** - Actionable insights

### 6 Integrated Analysis Tools
- 📍 **Carrier Optimization** - Smart carrier selection
- 🗺️ **Zone Analysis** - Zone-based optimization
- 🧠 **Smart Routing** - Intelligent routing decisions
- 🚀 **Express Lane** - Priority service routing
- 💰 **Cost Analysis** - Cost reduction opportunities
- ⭐ **Performance Scoring** - Carrier performance tracking

## 📁 File Upload Support

- **CSV Files** - Multiple encoding support
- **Excel Files** - .xlsx and .xls formats
- **FirstMile Column Mapping** - Automatic column recognition
- **Demo Data** - Built-in demo data generator

## 📊 Export Options

- **Excel Reports** - Comprehensive multi-sheet workbooks
- **CSV Summaries** - Quick data exports
- **PDF Reports** - Coming soon!
- **Dashboard Sharing** - Coming soon!

## 🔧 Technical Details

### Dependencies
- streamlit
- pandas
- numpy
- plotly
- xlsxwriter or openpyxl

### No Longer Required
- ❌ matplotlib
- ❌ seaborn
- ❌ Any gradient dependencies

## 💡 Usage Tips

1. **Upload Your Data**: Use the sidebar to upload FirstMile tracking reports
2. **Enable Tools**: Check the analysis tools you want to use
3. **Review Insights**: Navigate through all 11 sections
4. **Export Results**: Download Excel or CSV reports
5. **Debug Mode**: Enable for troubleshooting

## 🛠️ Troubleshooting

### Common Issues

**Issue**: "st.set_page_config() can only be called once"
- **Solution**: Already fixed! The dashboard now handles this properly.

**Issue**: Tables look cramped
- **Solution**: Already fixed! Tables now have proper 14px font and 12px padding.

**Issue**: Missing gradients/colors
- **Solution**: Already fixed! Using solid colors instead of gradients.

## 📈 Performance

- Analyzes 1000+ shipments in <1 second
- Real-time dashboard updates
- Efficient memory usage
- No heavy dependencies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Brett Walker**  
FirstMile - Shipping Without Limits  
20+ Years eCommerce Shipping Expertise

---

*FirstMile TransitIQ Enhanced v2.0 - Professional Shipping Analytics*
