# import streamlit as st
# from typing import Dict, Any, List
# import plotly.graph_objects as go
# import plotly.express as px
# from config.settings import Settings

# def render_header():
#     """Render the application header"""
#     # Header is now integrated into the main page design
#     pass

# def render_navbar():
#     """Render the navigation bar"""
#     st.markdown("""
#     <div class="navbar">
#         <div class="navbar-content">
#             <div class="navbar-left">
#                 <a href="/" class="navbar-logo">
#                     <svg width="32" height="32" viewBox="0 0 32 32" class="logo-icon">
#                         <circle cx="16" cy="16" r="14" fill="#4285F4" opacity="0.1"/>
#                         <path d="M16 6 C8 6 8 16 16 16 C24 16 24 26 16 26" stroke="#4285F4" stroke-width="3" fill="none"/>
#                         <circle cx="16" cy="11" r="3" fill="#EA4335"/>
#                         <circle cx="16" cy="21" r="3" fill="#34A853"/>
#                     </svg>
#                     <span class="navbar-title">Psyte</span>
#                 </a>
#             </div>
#             <div class="navbar-center">
#                 <!-- Future navigation items will go here -->
#             </div>
#             <div class="navbar-right">
#                 <button class="navbar-user-icon">
#                     <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
#                         <circle cx="14" cy="14" r="13" stroke="currentColor" stroke-width="2"/>
#                         <circle cx="14" cy="11" r="4" stroke="currentColor" stroke-width="2"/>
#                         <path d="M6 24 Q6 19 14 19 Q22 19 22 24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
#                     </svg>
#                 </button>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# def render_input_section():
#     """Render the input section - handled in main app"""
#     pass

# def render_results_section(results: Dict[str, Any]):
#     """Render the analysis results"""
#     summary = results.get("summary", {})
#     citations = results.get("citations", [])
#     missing_refs = results.get("missing_references", [])
    
#     # Summary metrics
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         st.metric(
#             "Total Citations",
#             summary.get("total_citations", 0)
#         )
    
#     with col2:
#         valid_count = summary.get("valid_citations", 0)
#         validity_score = summary.get("validity_score", 0)
#         st.metric(
#             "Valid Citations",
#             valid_count,
#             delta=f"{validity_score:.1f}%"
#         )
    
#     with col3:
#         issues_count = summary.get("invalid_citations", 0) + summary.get("uncertain_citations", 0)
#         st.metric(
#             "Issues Found",
#             issues_count,
#             delta_color="inverse"
#         )
    
#     with col4:
#         if 'web_enhanced_citations' in summary:
#             st.metric(
#                 "Web Enhanced",
#                 summary.get("web_enhanced_citations", 0),
#                 delta="with web search"
#             )
#         else:
#             confidence = summary.get("average_confidence", 0)
#             st.metric(
#                 "Confidence",
#                 f"{confidence:.1%}"
#             )
    
#     # Missing references alert if found
#     if missing_refs:
#         st.warning(f"Found {len(missing_refs)} potential statements that may need citations")
    
#     # Analysis tabs
#     if citations or missing_refs:
#         st.markdown("### Citation Analysis")
        
#         tabs = ["Overview", "Detailed Analysis", "Recommendations"]
#         if missing_refs:
#             tabs.append("Missing Citations")
        
#         tab_objects = st.tabs(tabs)
        
#         with tab_objects[0]:  # Overview
#             # Style detection
#             if summary.get("detected_style") != "unknown":
#                 st.info(f"Detected citation style: **{summary['detected_style'].upper()}**")
            
#             # Validity chart
#             col1, col2 = st.columns([2, 1])
#             with col1:
#                 fig_pie = create_validity_pie_chart(summary)
#                 st.plotly_chart(fig_pie, use_container_width=True)
            
#             with col2:
#                 st.markdown("#### Summary Statistics")
#                 st.markdown(f"""
#                 - **Analysis Date:** {summary.get('analysis_timestamp', 'N/A')[:10]}
#                 - **Text Length:** {results.get('text_length', 0):,} characters
#                 - **Citation Density:** {results.get('citation_density', 0):.2f} per 100 words
#                 """)
#                 if 'web_enhanced_citations' in summary:
#                     st.markdown(f"- **Web Enhanced:** {summary['web_enhanced_citations']} citations")
        
#         with tab_objects[1]:  # Detailed Analysis
#             # Detailed citation analysis
#             for i, citation in enumerate(citations):
#                 render_citation_card(citation, i)
        
#         with tab_objects[2]:  # Recommendations
#             # Recommendations
#             render_recommendations(results)
        
#         if missing_refs and len(tab_objects) > 3:
#             with tab_objects[3]:  # Missing Citations
#                 render_missing_references(missing_refs)

# def render_citation_card(citation: Dict[str, Any], index: int):
#     """Render a single citation analysis card"""
#     with st.expander(
#         f"Citation {index + 1}: {citation['text'][:60]}...",
#         expanded=False
#     ):
#         col1, col2 = st.columns([3, 1])
        
#         with col1:
#             # Citation text
#             st.markdown("**Citation Text:**")
#             st.code(citation['text'], language=None)
            
#             # Issues
#             if citation.get('issues'):
#                 st.markdown("**Issues Found:**")
#                 for issue in citation['issues']:
#                     st.markdown(f"- {issue}")
#             else:
#                 st.success("No issues found")
            
#             # Suggestions
#             if citation.get('suggestions'):
#                 st.markdown("**Suggestions:**")
#                 for suggestion in citation['suggestions']:
#                     st.markdown(f"- {suggestion}")
        
#         with col2:
#             # Status
#             if citation.get('is_valid'):
#                 st.success("Valid Citation")
#             elif citation.get('is_valid') is False:
#                 st.error("Invalid Citation")
#             else:
#                 st.warning("Uncertain Status")
            
#             # Confidence score
#             confidence = citation.get('confidence_score', 0)
#             st.markdown(f"**Confidence:** {confidence:.1%}")
#             st.progress(confidence)
            
#             # Style
#             st.markdown(f"**Style:** {citation.get('style', 'unknown').upper()}")
            
#             # Model used (if available)
#             model_used = citation.get('model_used')
#             if model_used:
#                 st.markdown(f"**Model:** {model_used}")
            
#             # Web search results if available
#             if 'web_search' in citation and citation['web_search']['found']:
#                 st.markdown("**Web Search:**")
#                 st.success("Found matching sources")
                
#             # Suggested format if available
#             if 'suggested_format' in citation:
#                 st.markdown("**Suggested Format:**")
#                 st.code(citation['suggested_format'], language=None)

# def render_recommendations(results: Dict[str, Any]):
#     """Render recommendations section"""
#     recommendations = results.get("recommendations", [])
#     common_issues = results.get("common_issues", [])
    
#     if recommendations:
#         st.markdown("### Recommendations")
#         for i, rec in enumerate(recommendations, 1):
#             st.markdown(f"{i}. {rec}")
    
#     if common_issues:
#         st.markdown("### Common Issues")
        
#         # Create a bar chart of common issues
#         if len(common_issues) > 0:
#             issues = [issue[0] for issue in common_issues[:5]]
#             counts = [issue[1] for issue in common_issues[:5]]
            
#             fig = px.bar(
#                 x=counts,
#                 y=issues,
#                 orientation='h',
#                 labels={'x': 'Frequency', 'y': 'Issue Type'},
#                 color_discrete_sequence=['#1a73e8']
#             )
#             fig.update_layout(
#                 height=300,
#                 plot_bgcolor='rgba(0,0,0,0)',
#                 paper_bgcolor='rgba(0,0,0,0)',
#                 showlegend=False,
#                 margin=dict(t=40, b=40, l=40, r=40)
#             )
#             fig.update_xaxes(gridcolor='rgba(128,128,128,0.2)')
#             fig.update_yaxes(gridcolor='rgba(128,128,128,0.2)')
#             st.plotly_chart(fig, use_container_width=True)

# def render_missing_references(missing_refs: List[Dict[str, Any]]):
#     """Render missing references section"""
#     st.markdown("### Potential Missing Citations")
#     st.markdown("These statements may need citations based on academic writing standards:")
    
#     for i, ref in enumerate(missing_refs):
#         with st.expander(f"Statement {i + 1}: \"{ref['text'][:60]}...\""):
#             st.markdown(f"**Full text:** {ref['text']}")
#             st.markdown(f"**Position in document:** Character {ref['position']}")
#             st.info(ref['suggestion'])
            
#             if 'suggested_citations' in ref and ref['suggested_citations']:
#                 st.markdown("**Suggested sources from web search:**")
#                 for j, source in enumerate(ref['suggested_citations'][:3]):
#                     st.markdown(f"{j + 1}. **{source.get('title', 'Unknown Title')}**")
#                     if source.get('authors'):
#                         st.markdown(f"   - Authors: {', '.join(source['authors'][:3])}")
#                     if source.get('year'):
#                         st.markdown(f"   - Year: {source['year']}")
#                     if source.get('doi'):
#                         st.markdown(f"   - DOI: [{source['doi']}](https://doi.org/{source['doi']})")
#                     st.markdown("---")

# def create_validity_pie_chart(summary: Dict[str, Any]) -> go.Figure:
#     """Create a pie chart showing citation validity distribution"""
#     labels = ['Valid', 'Invalid', 'Uncertain']
#     values = [
#         summary.get('valid_citations', 0),
#         summary.get('invalid_citations', 0),
#         summary.get('uncertain_citations', 0)
#     ]
#     colors = ['#34a853', '#ea4335', '#fbbc04']  # Google colors
    
#     fig = go.Figure(data=[go.Pie(
#         labels=labels,
#         values=values,
#         hole=0.4,
#         marker_colors=colors,
#         textposition='inside',
#         textinfo='percent+label',
#         hovertemplate='%{label}: %{value}<br>%{percent}<extra></extra>',
#         textfont=dict(size=14, color='white')
#     )])
    
#     fig.update_layout(
#         title={
#             'text': "Citation Validity Distribution",
#             'font': {'size': 16}
#         },
#         showlegend=True,
#         height=350,
#         plot_bgcolor='rgba(0,0,0,0)',
#         paper_bgcolor='rgba(0,0,0,0)',
#         font=dict(size=14),
#         margin=dict(t=60, b=20, l=20, r=20),
#         legend=dict(
#             bgcolor='rgba(0,0,0,0)',
#             bordercolor='rgba(0,0,0,0)'
#         )
#     )
    
#     return fig

# def test_connection(provider: str, api_key: str, use_mcp: bool):
#     """Test API connections"""
#     with st.spinner("Testing connections..."):
#         results = []
        
#         # Test AI provider
#         try:
#             if provider == "groq":
#                 from src.ai_providers import GroqProvider
#                 provider_obj = GroqProvider(api_key)
#             else:
#                 from src.ai_providers import GeminiProvider
#                 provider_obj = GeminiProvider(api_key)
            
#             if provider_obj.check_connection():
#                 results.append(("Success", f"{provider.title()} API", "Connected"))
#             else:
#                 results.append(("Error", f"{provider.title()} API", "Failed"))
#         except Exception as e:
#             results.append(("Error", f"{provider.title()} API", str(e)))
        
#         # Test MCP if enabled
#         if use_mcp:
#             try:
#                 from src.mcp_server import MCPServer
#                 mcp = MCPServer()
#                 if mcp.check_connection():
#                     results.append(("Success", "MCP Server", "Connected"))
#                 else:
#                     results.append(("Warning", "MCP Server", "Not available"))
#             except Exception as e:
#                 results.append(("Warning", "MCP Server", "Optional - Not configured"))
        
#         # Display results
#         for status, service, message in results:
#             if status == "Success":
#                 st.success(f"**{service}**: {message}")
#             elif status == "Error":
#                 st.error(f"**{service}**: {message}")
#             else:
#                 st.warning(f"**{service}**: {message}")

import streamlit as st
from typing import Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px
from config.settings import Settings

def render_header():
    """Render the application header"""
    # Header is now integrated into the main page design
    pass

def render_navbar():
    """Render the navigation bar"""
    st.markdown("""
    <div class="navbar">
        <div class="navbar-content">
            <div class="navbar-left">
                <a href="/" class="navbar-logo">
                    <svg width="32" height="32" viewBox="0 0 32 32" class="logo-icon">
                        <circle cx="16" cy="16" r="14" fill="#4285F4" opacity="0.1"/>
                        <path d="M16 6 C8 6 8 16 16 16 C24 16 24 26 16 26" stroke="#4285F4" stroke-width="3" fill="none"/>
                        <circle cx="16" cy="11" r="3" fill="#EA4335"/>
                        <circle cx="16" cy="21" r="3" fill="#34A853"/>
                    </svg>
                    <span class="navbar-title">Psyte</span>
                </a>
            </div>
            <div class="navbar-center">
                <!-- Future navigation items will go here -->
            </div>
            <div class="navbar-right">
                <button class="navbar-user-icon">
                    <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                        <circle cx="14" cy="14" r="13" stroke="currentColor" stroke-width="2"/>
                        <circle cx="14" cy="11" r="4" stroke="currentColor" stroke-width="2"/>
                        <path d="M6 24 Q6 19 14 19 Q22 19 22 24" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_input_section():
    """Render the input section - handled in main app"""
    pass

def render_results_section(results: Dict[str, Any]):
    """Render the analysis results"""
    summary = results.get("summary", {})
    citations = results.get("citations", [])
    missing_refs = results.get("missing_references", [])
    doi_validation = results.get("doi_validation", {})
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Citations",
            summary.get("total_citations", 0)
        )
    
    with col2:
        valid_count = summary.get("valid_citations", 0)
        validity_score = summary.get("validity_score", 0)
        st.metric(
            "Valid Citations",
            valid_count,
            delta=f"{validity_score:.1f}%"
        )
    
    with col3:
        issues_count = summary.get("invalid_citations", 0) + summary.get("uncertain_citations", 0)
        st.metric(
            "Issues Found",
            issues_count,
            delta_color="inverse"
        )
    
    with col4:
        if doi_validation:
            st.metric(
                "DOIs Found",
                doi_validation.get("total_dois_found", 0),
                delta=f"{doi_validation.get('valid_dois', 0)} valid"
            )
        elif 'web_enhanced_citations' in summary:
            st.metric(
                "Web Enhanced",
                summary.get("web_enhanced_citations", 0),
                delta="with web search"
            )
        else:
            confidence = summary.get("average_confidence", 0)
            st.metric(
                "Confidence",
                f"{confidence:.1%}"
            )
    
    # DOI Validation Results
    if doi_validation and doi_validation.get('total_dois_found', 0) > 0:
        with st.expander("🔗 DOI Validation Results", expanded=True):
            st.markdown(f"**Found {doi_validation['total_dois_found']} DOI(s)**")
            st.markdown(f"- ✅ Valid: {doi_validation['valid_dois']}")
            st.markdown(f"- ❌ Invalid: {doi_validation['invalid_dois']}")
            
            st.markdown("---")
            
            for doi_result in doi_validation['results']:
                if doi_result['valid']:
                    with st.container():
                        st.success(f"✅ **{doi_result['doi']}**")
                        if doi_result.get('data'):
                            data = doi_result['data']
                            st.markdown(f"**Title:** {data.get('title', 'N/A')}")
                            authors = data.get('authors', [])
                            if authors:
                                author_names = ', '.join([a['full_name'] for a in authors[:3]])
                                if len(authors) > 3:
                                    author_names += f" et al. ({len(authors)} total)"
                                st.markdown(f"**Authors:** {author_names}")
                            st.markdown(f"**Published:** {data.get('date', {}).get('formatted', 'N/A')}")
                            st.markdown(f"**Journal:** {data.get('journal', 'N/A')}")
                            if data.get('citations'):
                                st.markdown(f"**Citations:** {data['citations']:,}")
                            st.markdown(f"**URL:** [{doi_result['doi']}]({data.get('url', '#')})")
                        st.markdown("")
                else:
                    st.error(f"❌ **{doi_result['doi']}**: {doi_result.get('error', 'Unknown error')}")
    
    # Missing references alert if found
    if missing_refs:
        st.warning(f"Found {len(missing_refs)} potential statements that may need citations")
    
    # Analysis tabs
    if citations or missing_refs:
        st.markdown("### Citation Analysis")
        
        tabs = ["Overview", "Detailed Analysis", "Recommendations"]
        if missing_refs:
            tabs.append("Missing Citations")
        
        tab_objects = st.tabs(tabs)
        
        with tab_objects[0]:  # Overview
            # Style detection
            if summary.get("detected_style") != "unknown":
                st.info(f"Detected citation style: **{summary['detected_style'].upper()}**")
            
            # Validity chart
            col1, col2 = st.columns([2, 1])
            with col1:
                fig_pie = create_validity_pie_chart(summary)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                st.markdown("#### Summary Statistics")
                st.markdown(f"""
                - **Analysis Date:** {summary.get('analysis_timestamp', 'N/A')[:10]}
                - **Text Length:** {results.get('text_length', 0):,} characters
                - **Citation Density:** {results.get('citation_density', 0):.2f} per 100 words
                """)
                if 'web_enhanced_citations' in summary:
                    st.markdown(f"- **Web Enhanced:** {summary['web_enhanced_citations']} citations")
                if doi_validation:
                    st.markdown(f"- **DOIs Found:** {doi_validation.get('total_dois_found', 0)}")
        
        with tab_objects[1]:  # Detailed Analysis
            # Detailed citation analysis
            for i, citation in enumerate(citations):
                render_citation_card(citation, i)
        
        with tab_objects[2]:  # Recommendations
            # Recommendations
            render_recommendations(results)
        
        if missing_refs and len(tab_objects) > 3:
            with tab_objects[3]:  # Missing Citations
                render_missing_references(missing_refs)

def render_citation_card(citation: Dict[str, Any], index: int):
    """Render a single citation analysis card"""
    # Format expander title
    citation_preview = citation['text'][:60] + "..." if len(citation['text']) > 60 else citation['text']
    
    # Add status emoji to title
    if citation.get('is_valid'):
        status_emoji = "✅"
    elif citation.get('is_valid') is False:
        status_emoji = "❌"
    else:
        status_emoji = "⚠️"
    
    with st.expander(
        f"{status_emoji} Citation {index + 1}: {citation_preview}",
        expanded=False
    ):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Citation text
            st.markdown("**Citation Text:**")
            st.code(citation['text'], language=None)
            
            # DOI Information
            if citation.get('doi'):
                st.markdown("**DOI Information:**")
                if citation.get('doi_valid'):
                    st.success(f"✅ Valid DOI: {citation['doi']}")
                    if citation.get('doi_data'):
                        doi_data = citation['doi_data']
                        st.markdown(f"- **Title:** {doi_data.get('title', 'N/A')}")
                        authors = doi_data.get('authors', [])
                        if authors:
                            author_str = ', '.join([a['full_name'] for a in authors[:2]])
                            if len(authors) > 2:
                                author_str += " et al."
                            st.markdown(f"- **Authors:** {author_str}")
                        st.markdown(f"- **Year:** {doi_data.get('date', {}).get('year', 'N/A')}")
                else:
                    st.error(f"❌ Invalid DOI: {citation['doi']}")
            
            # Issues
            if citation.get('issues'):
                st.markdown("**Issues Found:**")
                for issue in citation['issues']:
                    st.markdown(f"- {issue}")
            else:
                st.success("No issues found")
            
            # Suggestions
            if citation.get('suggestions'):
                st.markdown("**Suggestions:**")
                for suggestion in citation['suggestions']:
                    st.markdown(f"- {suggestion}")
        
        with col2:
            # Status
            if citation.get('is_valid'):
                st.success("Valid Citation")
            elif citation.get('is_valid') is False:
                st.error("Invalid Citation")
            else:
                st.warning("Uncertain Status")
            
            # Confidence score
            confidence = citation.get('confidence_score', 0)
            st.markdown(f"**Confidence:** {confidence:.1%}")
            st.progress(confidence)
            
            # Style
            st.markdown(f"**Style:** {citation.get('style', 'unknown').upper()}")
            
            # Model used (if available)
            model_used = citation.get('model_used')
            if model_used:
                st.markdown(f"**Model:** {model_used}")
            
            # Web search results if available
            if 'web_search' in citation and citation['web_search']['found']:
                st.markdown("**Web Search:**")
                st.success("Found matching sources")
                
            # Suggested format if available
            if 'suggested_format' in citation:
                st.markdown("**Suggested Format:**")
                st.code(citation['suggested_format'], language=None)

def render_recommendations(results: Dict[str, Any]):
    """Render recommendations section"""
    recommendations = results.get("recommendations", [])
    common_issues = results.get("common_issues", [])
    
    if recommendations:
        st.markdown("### Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    
    if common_issues:
        st.markdown("### Common Issues")
        
        # Create a bar chart of common issues
        if len(common_issues) > 0:
            issues = [issue[0] for issue in common_issues[:5]]
            counts = [issue[1] for issue in common_issues[:5]]
            
            fig = px.bar(
                x=counts,
                y=issues,
                orientation='h',
                labels={'x': 'Frequency', 'y': 'Issue Type'},
                color_discrete_sequence=['#1a73e8']
            )
            fig.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(t=40, b=40, l=40, r=40)
            )
            fig.update_xaxes(gridcolor='rgba(128,128,128,0.2)')
            fig.update_yaxes(gridcolor='rgba(128,128,128,0.2)')
            st.plotly_chart(fig, use_container_width=True)

def render_missing_references(missing_refs: List[Dict[str, Any]]):
    """Render missing references section"""
    st.markdown("### Potential Missing Citations")
    st.markdown("These statements may need citations based on academic writing standards:")
    
    for i, ref in enumerate(missing_refs):
        with st.expander(f"Statement {i + 1}: \"{ref['text'][:60]}...\""):
            st.markdown(f"**Full text:** {ref['text']}")
            st.markdown(f"**Position in document:** Character {ref['position']}")
            st.info(ref['suggestion'])
            
            if 'suggested_citations' in ref and ref['suggested_citations']:
                st.markdown("**Suggested sources from web search:**")
                for j, source in enumerate(ref['suggested_citations'][:3]):
                    st.markdown(f"{j + 1}. **{source.get('title', 'Unknown Title')}**")
                    if source.get('authors'):
                        st.markdown(f"   - Authors: {', '.join(source['authors'][:3])}")
                    if source.get('year'):
                        st.markdown(f"   - Year: {source['year']}")
                    if source.get('doi'):
                        st.markdown(f"   - DOI: [{source['doi']}](https://doi.org/{source['doi']})")
                    st.markdown("---")

def create_validity_pie_chart(summary: Dict[str, Any]) -> go.Figure:
    """Create a pie chart showing citation validity distribution"""
    labels = ['Valid', 'Invalid', 'Uncertain']
    values = [
        summary.get('valid_citations', 0),
        summary.get('invalid_citations', 0),
        summary.get('uncertain_citations', 0)
    ]
    colors = ['#34a853', '#ea4335', '#fbbc04']  # Google colors
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker_colors=colors,
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='%{label}: %{value}<br>%{percent}<extra></extra>',
        textfont=dict(size=14, color='white')
    )])
    
    fig.update_layout(
        title={
            'text': "Citation Validity Distribution",
            'font': {'size': 16}
        },
        showlegend=True,
        height=350,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        margin=dict(t=60, b=20, l=20, r=20),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        )
    )
    
    return fig

def test_connection(provider: str, api_key: str, use_mcp: bool):
    """Test API connections"""
    with st.spinner("Testing connections..."):
        results = []
        
        # Test AI provider
        try:
            if provider == "groq":
                from src.ai_providers import GroqProvider
                provider_obj = GroqProvider(api_key)
            else:
                from src.ai_providers import GeminiProvider
                provider_obj = GeminiProvider(api_key)
            
            if provider_obj.check_connection():
                results.append(("Success", f"{provider.title()} API", "Connected"))
            else:
                results.append(("Error", f"{provider.title()} API", "Failed"))
        except Exception as e:
            results.append(("Error", f"{provider.title()} API", str(e)))
        
        # Test MCP if enabled
        if use_mcp:
            try:
                from src.mcp_server import MCPServer
                mcp = MCPServer()
                if mcp.check_connection():
                    results.append(("Success", "MCP Server", "Connected"))
                else:
                    results.append(("Warning", "MCP Server", "Not available"))
            except Exception as e:
                results.append(("Warning", "MCP Server", "Optional - Not configured"))
        
        # Display results
        for status, service, message in results:
            if status == "Success":
                st.success(f"**{service}**: {message}")
            elif status == "Error":
                st.error(f"**{service}**: {message}")
            else:
                st.warning(f"**{service}**: {message}")