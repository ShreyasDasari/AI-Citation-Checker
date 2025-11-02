import streamlit as st
from typing import Dict, Any
from src.doi_validator import DOIValidator

def render_doi_validator():
    """Render DOI validation interface"""
    st.markdown("### DOI Validator")
    st.markdown("Enter a DOI to retrieve and validate publication information")
    
    # Initialize validator
    if 'doi_validator' not in st.session_state:
        st.session_state.doi_validator = DOIValidator()
    
    validator = st.session_state.doi_validator
    
    # Input section
    col1, col2 = st.columns([4, 1])
    
    with col1:
        doi_input = st.text_input(
            "DOI",
            placeholder="e.g., 10.1038/nature14539 or https://doi.org/10.1038/nature14539",
            label_visibility="collapsed",
            key="doi_input_field"
        )
    
    with col2:
        validate_button = st.button("Validate", type="primary", use_container_width=True)
    
    # Example DOIs
    st.markdown("**Examples:**")
    example_cols = st.columns(3)
    
    examples = [
        ("Deep Learning (Nature)", "10.1038/nature14539"),
        ("CRISPR (Science)", "10.1126/science.1127647"),
        ("Tangram (Nature Methods)", "10.1038/s41592-021-01264-7")
    ]
    
    for col, (label, doi) in zip(example_cols, examples):
        with col:
            if st.button(label, key=f"example_{doi}", use_container_width=True):
                st.session_state.doi_input_field = doi
                st.rerun()
    
    # Validate DOI
    if validate_button or (doi_input and 'last_validated_doi' not in st.session_state):
        if not doi_input:
            st.error("Please enter a DOI")
        else:
            with st.spinner("Searching CrossRef database..."):
                result = validator.get_publication_info(doi_input)
                st.session_state.last_doi_result = result
                st.session_state.last_validated_doi = doi_input
    
    # Display results
    if 'last_doi_result' in st.session_state:
        result = st.session_state.last_doi_result
        
        if result['success']:
            render_doi_success(result['data'], validator)
        else:
            st.error(f"❌ **Error:** {result['error']}")
            st.info(f"DOI: {result['doi']}")

def render_doi_success(data: Dict[str, Any], validator: DOIValidator):
    """Render successful DOI validation result"""
    st.success("✅ **Publication Found**")
    
    # Publication info
    st.markdown("---")
    
    # Title
    st.markdown(f"### {data['title']}")
    
    # Metadata grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Type:** {data['type']}")
        st.markdown(f"**Publisher:** {data['publisher']}")
        
        if data['journal']:
            st.markdown(f"**Journal:** {data['journal']}")
        
        if data['volume']:
            vol_info = f"Volume {data['volume']}"
            if data['issue']:
                vol_info += f", Issue {data['issue']}"
            if data['pages']:
                vol_info += f", pp. {data['pages']}"
            st.markdown(f"**Volume/Issue:** {vol_info}")
    
    with col2:
        st.markdown(f"**Published:** {data['date']['formatted']}")
        st.markdown(f"**Citations:** {data['citations']:,}")
        st.markdown(f"**DOI:** [{data.get('doi', 'N/A')}]({data['url']})")
    
    # Authors
    if data['authors']:
        st.markdown("**Authors:**")
        
        # Show first 5 authors
        author_names = [a['full_name'] for a in data['authors'][:5]]
        if len(data['authors']) > 5:
            author_names.append(f"... and {len(data['authors']) - 5} more")
        
        st.markdown(", ".join(author_names))
        
        # Show all authors in expander
        if len(data['authors']) > 5:
            with st.expander("View all authors"):
                for i, author in enumerate(data['authors'], 1):
                    st.markdown(f"{i}. {author['full_name']}")
    
    # Abstract
    if data.get('abstract'):
        with st.expander("Abstract"):
            st.markdown(data['abstract'])
    
    # Citation formats
    st.markdown("---")
    st.markdown("### 📋 Formatted Citations")
    
    citation_styles = ['APA', 'MLA', 'Chicago', 'Harvard', 'IEEE']
    selected_style = st.selectbox("Citation Style", citation_styles, key="citation_style_select")
    
    citation = validator.format_citation(data, selected_style.lower())
    
    st.code(citation, language=None)
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("📋 Copy Citation", use_container_width=True):
            st.write("Citation copied to clipboard!")
            st.session_state.clipboard = citation
    
    # Additional metadata
    with st.expander("Additional Metadata"):
        if data.get('subjects'):
            st.markdown(f"**Subjects:** {', '.join(data['subjects'])}")
        
        if data.get('issn'):
            st.markdown(f"**ISSN:** {', '.join(data['issn'])}")
        
        if data.get('isbn'):
            st.markdown(f"**ISBN:** {', '.join(data['isbn'])}")
        
        if data.get('license'):
            st.markdown("**License:**")
            for lic in data['license']:
                if lic['url']:
                    st.markdown(f"- [{lic['url']}]({lic['url']})")

def render_doi_extractor():
    """Render DOI extraction from text"""
    st.markdown("### Extract DOIs from Text")
    st.markdown("Paste text containing DOIs to extract and validate them")
    
    text_input = st.text_area(
        "Text with DOIs",
        height=200,
        placeholder="Paste your text containing DOIs here...",
        label_visibility="collapsed"
    )
    
    if st.button("Extract DOIs", type="primary"):
        if not text_input:
            st.warning("Please enter some text")
        else:
            validator = DOIValidator()
            dois = validator.extract_dois_from_text(text_input)
            
            if not dois:
                st.info("No DOIs found in the text")
            else:
                st.success(f"Found {len(dois)} DOI(s)")
                
                for i, doi in enumerate(dois, 1):
                    with st.expander(f"DOI {i}: {doi}"):
                        with st.spinner("Validating..."):
                            result = validator.get_publication_info(doi)
                            
                            if result['success']:
                                data = result['data']
                                st.markdown(f"**Title:** {data['title']}")
                                st.markdown(f"**Authors:** {', '.join([a['full_name'] for a in data['authors'][:3]])}{'...' if len(data['authors']) > 3 else ''}")
                                st.markdown(f"**Published:** {data['date']['formatted']}")
                                st.markdown(f"**Journal:** {data['journal']}")
                                
                                citation = validator.format_citation(data, 'apa')
                                st.code(citation, language=None)
                            else:
                                st.error(f"Error: {result['error']}")