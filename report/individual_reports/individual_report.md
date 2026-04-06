# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Phan Văn Tấn
- **Student ID**: 2A202600282
- **Date**: 06/04/2026

## I. Technical Contribution (15 Points)
- **Modules Implementated**: `src/tools/reader.py`
- **Code Highlights**: 

    def clean_text(text: str) -> str:

        """
            Clean text by removing or normalizing strange characters.
            Args:
                text: Input text to clean 
            Returns:
                Cleaned text with normalized unicode and removed control characters
        """

    def extract_abstract(text: str, max_sentences: int = 5) -> Optional[str]:

        """
            Extract abstract from text. Looks for an explicit Abstract section or 
            extracts the first paragraph if no abstract is found.
            Args:
                text: Full text to extract abstract from
                max_sentences: Maximum number of sentences to include if no explicit abstract
            Returns:
                Extracted abstract or None if text is empty
        """

    def extract_metadata(text: str) -> Dict[str, Any]:

        """
            Extract metadata from text (title, authors, abstract, etc.)
            Args:
                text: Input text to extract metadata from 
            Returns:
                Dictionary with extracted metadata
        """
- **Documentation**:     
  + Hai công cụ extract_abstract và extract_metadata giúp agent trích xuất abstract và metadata từ nội dung bài báo thô.

  + Khi agent nhận thấy cần tóm tắt hoặc dữ liệu cấu trúc, nó sẽ gọi công cụ, nhận kết quả trả về và dùng làm Observation trong vòng lặp ReAct.

  + Nhờ đó, agent có thông tin sạch và có cấu trúc để ra quyết định chính xác hơn, giảm khả năng hallucinates.
  
## II. Debugging Case Study (10 Points)
- **Problem Description**: 
- 
## III. Personal Insights: Chatbot vs ReAct (10 Points)