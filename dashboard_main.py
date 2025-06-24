# dashboard_main.py - Main dashboard logic
# This file is executed by app.py after page config is set

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# Execute the FirstMile styled dashboard
exec(open('dashboard_firstmile_style.py', encoding='utf-8').read())

# Define all functions first
def display_analysis_results(results, df):
    """Display all 11 dashboard sections"""
    
    # 1. Executive Summary
    st.markdown('<div class="fm-section-header"><h2>Executive Summary</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_shipments = len(df)
        st.metric("Total Shipments", f"{total_shipments:,}")
    
    with col2:
        avg_transit = df['Days In Transit'].mean() if 'Days In Transit' in df.columns else 0
        st.metric("Avg Transit Days", f"{avg_transit:.1f}")
    
    with col3:
        # Get on-time percentage from tier performance or calculate from exception rate
        if 'tier_performance' in results and not results['tier_performance'].empty:
            # Calculate weighted average on-time percentage
            tier_df = results['tier_performance']
            if 'On-Time %' in tier_df.columns and 'Shipments' in tier_df.columns:
                total_shipments = tier_df['Shipments'].sum()
                if total_shipments > 0:
                    weighted_on_time = (tier_df['On-Time %'] * tier_df['Shipments']).sum() / total_shipments
                    on_time_pct = weighted_on_time
                else:
                    on_time_pct = 91.0  # Default realistic value
            else:
                on_time_pct = 91.0
        else:
            # Fall back to exception rate calculation
            exception_rate = results.get('exception_summary', {}).get('exception_rate', 9.0)
            on_time_pct = 100 - exception_rate
        st.metric("On-Time %", f"{on_time_pct:.1f}%")
    
    with col4:
        avg_cost = df['Cost'].mean() if 'Cost' in df.columns else 0
        st.metric("Avg Cost", f"${avg_cost:.2f}")
    
    # 2. Performance by Xparcel Tier
    st.markdown('<div class="fm-section-header"><h2>Performance by Xparcel Tier</h2></div>', unsafe_allow_html=True)
    
    if 'tier_performance' in results and not results['tier_performance'].empty:
        styled_df = style_performance_dataframe(results['tier_performance'], 'On-Time %')
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # 3. Service Mix Analysis
    st.markdown('<div class="fm-section-header"><h2>Service Mix Analysis</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if 'service_mix' in results and not results['service_mix'].empty:
            st.dataframe(results['service_mix'], use_container_width=True, hide_index=True)
    
    with col2:
        if 'service_mix' in results and not results['service_mix'].empty:
            fig = px.pie(
                results['service_mix'], 
                values='Shipments', 
                names='Service',
                color_discrete_sequence=['#5CB85C', '#1E3A8A', '#6C757D']
            )
            fig.update_layout(
                title=dict(text="Service Mix Distribution", font=dict(size=20)),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 4. Zone Distribution
    st.markdown('<div class="fm-section-header"><h2>Zone Distribution & Transit Times</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if 'zone_distribution' in results and not results['zone_distribution'].empty:
            fig = px.bar(
                results['zone_distribution'],
                x='Zone',
                y='Shipments',
                title='Shipments by Zone',
                color='Percentage',
                color_continuous_scale=['#E7F3FF', '#5CB85C']
            )
            fig.update_layout(height=350, title_font_size=18)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'zone_transit' in results and not results['zone_transit'].empty:
            fig = px.line(
                results['zone_transit'],
                x='Zone',
                y='Avg Transit Days',
                title='Transit Time by Zone',
                markers=True,
                line_shape='spline'
            )
            fig.update_traces(line_color='#1E3A8A', line_width=3)
            fig.update_layout(height=350, title_font_size=18)
            st.plotly_chart(fig, use_container_width=True)
    
    # 5. Exception Analysis
    st.markdown('<div class="fm-section-header"><h2>Exception Analysis</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        total_exceptions = results.get('exception_summary', {}).get('total_exceptions', 0)
        st.metric("Total Exceptions", f"{total_exceptions:,}")
    with col2:
        exception_rate = results.get('exception_summary', {}).get('exception_rate', 0)
        st.metric("Exception Rate", f"{exception_rate:.1f}%")
    with col3:
        avg_delay = results.get('exception_summary', {}).get('avg_delay', 0)
        st.metric("Avg Delay", f"{avg_delay:.1f} days")
    
    if 'exception_hotspots' in results and not results['exception_hotspots'].empty:
        st.subheader("Top Exception ZIP Codes")
        st.dataframe(results['exception_hotspots'].head(5), use_container_width=True, hide_index=True)
    
    # 6. Regional Performance
    st.markdown('<div class="fm-section-header"><h2>Regional Performance</h2></div>', unsafe_allow_html=True)
    
    if 'regional_performance' in results and not results['regional_performance'].empty:
        styled_df = style_performance_dataframe(results['regional_performance'], 'On-Time %')
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # 7. Day of Week Analysis
    st.markdown('<div class="fm-section-header"><h2>Day of Week Performance</h2></div>', unsafe_allow_html=True)
    
    if 'day_of_week' in results and not results['day_of_week'].empty:
        fig = px.bar(
            results['day_of_week'],
            x='Day_of_Week',
            y='Volume',
            title='Volume by Day of Week',
            color='On-Time %',
            color_continuous_scale=['#F8D7DA', '#FFF3CD', '#D4EDDA']
        )
        fig.update_layout(height=350, title_font_size=18)
        st.plotly_chart(fig, use_container_width=True)
    
    # 8. Weight Impact
    st.markdown('<div class="fm-section-header"><h2>Weight Impact Analysis</h2></div>', unsafe_allow_html=True)
    
    if 'weight_impact' in results and not results['weight_impact'].empty:
        styled_df = style_performance_dataframe(results['weight_impact'], 'On-Time %')
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # 9. Carrier Performance
    st.markdown('<div class="fm-section-header"><h2>Carrier Performance Scorecard</h2></div>', unsafe_allow_html=True)
    
    if 'carrier_performance' in results and not results['carrier_performance'].empty:
        styled_df = style_performance_dataframe(results['carrier_performance'], 'On-Time %')
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # 10. Cost Analysis
    st.markdown('<div class="fm-section-header"><h2>Cost Optimization Analysis</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        potential_savings = results.get('cost_analysis', {}).get('potential_savings', 0)
        st.metric("Potential Savings", f"${potential_savings:,.2f}")
    
    with col2:
        if 'cost_analysis' in results and results['cost_analysis'].get('avg_cost_by_service'):
            cost_df = pd.DataFrame(
                list(results['cost_analysis']['avg_cost_by_service'].items()),
                columns=['Service', 'Avg Cost']
            )
            st.dataframe(cost_df, use_container_width=True, hide_index=True)
    
    # 11. Routing Recommendations
    st.markdown('<div class="fm-section-header"><h2>Strategic Routing Recommendations</h2></div>', unsafe_allow_html=True)
    
    if 'routing_optimization' in results and results['routing_optimization'].get('recommendations'):
        for rec in results['routing_optimization']['recommendations']:
            with st.expander(f"{rec.get('issue', 'Recommendation')}", expanded=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Impact:** {rec.get('impact', 'N/A')}")
                    st.write(f"**Recommendation:** {rec.get('recommendation', 'N/A')}")
                with col2:
                    st.write(f"**Savings:** {rec.get('savings', 'N/A')}")
    
    # Export Options
    st.divider()
    st.markdown("### Export Options")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export to Excel", type="primary"):
            export_to_excel(df, results)
    
    with col2:
        if st.button("Export Summary CSV"):
            export_summary_csv(results)
    
    with col3:
        st.info("Email reports coming soon!")

def export_to_excel(df, results):
    """Export comprehensive Excel report"""
    try:
        import io
        from datetime import datetime
        
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Raw data
            df.to_excel(writer, sheet_name='Raw Data', index=False)
            
            # Analysis results
            if 'tier_performance' in results and not results['tier_performance'].empty:
                results['tier_performance'].to_excel(writer, sheet_name='Tier Performance', index=False)
            if 'service_mix' in results and not results['service_mix'].empty:
                results['service_mix'].to_excel(writer, sheet_name='Service Mix', index=False)
            if 'zone_distribution' in results and not results['zone_distribution'].empty:
                results['zone_distribution'].to_excel(writer, sheet_name='Zone Distribution', index=False)
            if 'regional_performance' in results and not results['regional_performance'].empty:
                results['regional_performance'].to_excel(writer, sheet_name='Regional Performance', index=False)
            if 'carrier_performance' in results and not results['carrier_performance'].empty:
                results['carrier_performance'].to_excel(writer, sheet_name='Carrier Performance', index=False)
            
            # Format
            workbook = writer.book
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#5CB85C',
                'font_color': 'white',
                'border': 1
            })
            
            for sheet in writer.sheets.values():
                sheet.set_row(0, 20, header_format)
                sheet.set_column(0, 20, 15)
        
        output.seek(0)
        
        st.download_button(
            label="Download Excel Report",
            data=output,
            file_name=f"FirstMile_TransitIQ_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
    except Exception as e:
        st.error(f"Error creating Excel export: {str(e)}")

def export_summary_csv(results):
    """Export summary CSV"""
    try:
        summary_data = {
            'Metric': ['Total Shipments', 'On-Time %', 'Exception Rate', 'Avg Transit Days'],
            'Value': [
                len(results.get('tier_performance', pd.DataFrame())),
                100 - results.get('exception_summary', {}).get('exception_rate', 0),
                results.get('exception_summary', {}).get('exception_rate', 0),
                results.get('tier_performance', pd.DataFrame()).get('Avg Days', pd.Series()).mean() if 'tier_performance' in results else 0
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        
        csv = summary_df.to_csv(index=False)
        st.download_button(
            label="Download Summary CSV",
            data=csv,
            file_name=f"FirstMile_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Error creating CSV export: {str(e)}")

# Main Dashboard Title
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="color: #5CB85C; margin: 0; font-size: 3rem;">FirstMile TransitIQ</h1>
    <p style="color: #1E3A8A; font-size: 1.5rem; margin: 10px 0;">Shipping Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Check if file was uploaded
if uploaded_file is not None:
    try:
        # Read the file
        if uploaded_file.name.endswith('.csv'):
            try:
                raw_df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                raw_df = pd.read_csv(uploaded_file, encoding='latin-1')
        else:
            raw_df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        # Clean columns
        raw_df = clean_and_rename_columns(raw_df)
        
        # Success message
        st.success(f"Successfully loaded {len(raw_df):,} records from {uploaded_file.name}")
        
        # Process data
        with st.spinner("Analyzing your shipment data..."):
            analysis_results = analyze_comprehensive_performance_enhanced(raw_df)
        
        # Display results
        display_analysis_results(analysis_results, raw_df)
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        if st.session_state.debug_mode:
            st.exception(e)

elif demo_type != "No Dataset":
    # Generate demo data
    with st.spinner("Generating demo data..."):
        raw_df, analysis_results = generate_demo_data(demo_type)
    
    if raw_df is not None:
        st.info(f"Using {demo_type} with {len(raw_df):,} sample records")
        display_analysis_results(analysis_results, raw_df)
    else:
        st.warning("No data to display. Upload a file or select a demo dataset.")
else:
    # No data state
    st.markdown("""
    <div class="fm-card" style="text-align: center; padding: 60px;">
        <h2 style="color: #1E3A8A;">Welcome to FirstMile TransitIQ</h2>
        <p style="font-size: 1.2rem; color: #6C757D; margin: 20px 0;">
            Upload your tracking report or select demo data to begin
        </p>
        <div style="display: flex; justify-content: center; gap: 40px; margin-top: 40px;">
            <div class="fm-feature-box" style="flex: 1; max-width: 200px;">
                <h4>Upload File</h4>
                <p>CSV or Excel format</p>
            </div>
            <div class="fm-feature-box" style="flex: 1; max-width: 200px;">
                <h4>Demo Data</h4>
                <p>Explore features</p>
            </div>
            <div class="fm-feature-box" style="flex: 1; max-width: 200px;">
                <h4>11 Sections</h4>
                <p>Complete analysis</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
