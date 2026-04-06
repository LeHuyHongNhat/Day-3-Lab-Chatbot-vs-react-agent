from src.tools.search import search_arxiv, get_paper_abstract
from src.tools.reader import clean_text, extract_abstract, extract_metadata


if __name__ == "__main__":
    print("=" * 70)
    print("Demo: ArXiv Search & Text Processing Tools")
    print("=" * 70)
    
    # Demo 1: Search ArXiv
    print("\n[Demo 1] Searching ArXiv for 'machine learning'...")
    query = "machine learning"
    result = search_arxiv(query, max_results=2)
    print(result)
    
    # Demo 2: Get paper abstract
    print("\n[Demo 2] Fetching paper abstract...")
    paper_id = "2401.12345v1"
    abstract_result = get_paper_abstract(paper_id)
    print(abstract_result)
    
    # Demo 3: Clean text
    print("\n[Demo 3] Cleaning text...")
    messy_text = "  Hello    world  \n\n  This is  a   test  "
    cleaned = clean_text(messy_text)
    print(f"Original: '{messy_text}'")
    print(f"Cleaned: '{cleaned}'")
    
    # Demo 4: Extract abstract
    print("\n[Demo 4] Extracting abstract...")
    sample_text = """
    Title: Machine Learning Applications
    
    Abstract: This paper discusses machine learning techniques and applications.
    
    Introduction: Machine learning is transforming industries worldwide.
    """
    extracted = extract_abstract(sample_text)
    print(f"Extracted: {extracted}")
    
    # Demo 5: Extract metadata
    print("\n[Demo 5] Extracting metadata...")
    metadata = extract_metadata(sample_text)
    for key, value in metadata.items():
        if isinstance(value, str) and len(value) > 60:
            print(f"{key}: {value[:60]}...")
        else:
            print(f"{key}: {value}")
    
    print("\n" + "=" * 70)
    print("Demo complete!")
    print("=" * 70)