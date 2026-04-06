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
- **Problem Description**: Trong quá trình yêu cầu agent tìm các paper về momentum stocks 2024, agent liên tục gọi các tool với tham số sai. Ví dụ, agent dùng key="..." trong search_arxiv() hoặc get_paper_abstract(), nhưng các hàm này yêu cầu query hoặc paper_id. Kết quả là liên tục báo lỗi:
  
        [Error] search_arxiv() got an unexpected keyword argument 'key'
        [Error] search_arxiv() missing 1 required positional argument: 'query'
        [Error] get_paper_abstract() got an unexpected keyword argument 'key'
        Error fetching paper 0402134: 400 Client Error

- **Log Source**:  
         
        {"timestamp": "2026-04-06T09:52:33.866259", "event": "TOOL_CALL", "data": {"tool": "search_arxiv", "args": "key=\"momentum US stock 2024 momentum strategies equity 2024\"", "observation": "[Error] search_arxiv() got an unexpected keyword argument 'key'"}}
        {"timestamp": "2026-04-06T09:52:40.644079", "event": "TOOL_CALL", "data": {"tool": "search_arxiv", "args": "\"momentum 2024 US equities momentum strategies US stocks 2024\"", "observation": "[Error] search_arxiv() missing 1 required positional argument: 'query'"}}

- **Diagnosis**: Nguyên nhân: Agent không biết đúng tham số cần dùng cho các tool, dẫn đến gọi sai hàm. Có thể do:
    + Prompt hoặc system prompt chưa hướng dẫn agent cách sử dụng query và paper_id.
    + LLM chưa học cách xử lý khi tool call thất bại.
    + Một số bước tìm kiếm quá chi tiết, khiến ArXiv không trả về kết quả (No papers found), agent lại cố tìm bằng query khác.
- **Solution**:
  	
    + Chuẩn hóa prompt để hướng dẫn agent sử dụng đúng tham số: search_arxiv(query: str) và get_paper_abstract(paper_id: str).
	+ Thêm cơ chế bắt lỗi trong agent: nếu tool call thất bại, agent ghi log, thử query đơn giản hơn hoặc dùng fallback plan (ví dụ trả về kiến thức nền có sẵn).
	+ Kiểm tra và validate tham số trước khi gọi tool, tránh gửi key không hợp lệ.
	+ Tối ưu hóa query: agent nên bắt đầu với query tổng quát, sau đó refine từng bước dựa trên kết quả observation.
## III. Personal Insights: Chatbot vs ReAct (10 Points)
1.  **Reasoning**: 
    Khối Thought trong ReAct giúp tác nhân lập luận rõ ràng trước khi thực hiện hành động. Khác với Chatbot trả lời trực tiếp, Thought giúp:
        •	Lập kế hoạch: Chia yêu cầu phức tạp thành các bước nhỏ, ví dụ trước khi lấy abstract về ý tưởng trading momentum, tác nhân cân nhắc các truy vấn phù hợp.
        •	Tự đánh giá: Dự đoán vấn đề có thể xảy ra, ví dụ “truy vấn trước quá cụ thể” và điều chỉnh chiến lược.
        •	Minh bạch: Mỗi Thought giải thích lý do chọn hành động, giúp theo dõi quá trình suy luận.

    Nói cách khác, Thought biến khả năng lý luận thành quá trình từng bước, quan sát được, giúp giải quyết vấn đề có hệ thống hơn Chatbot trả lời trực tiếp.

2. **Reliability**: 
    Agent đôi khi thua Chatbot vì:
        •	Quá phụ thuộc vào công cụ: Khi search_arxiv hoặc get_paper_abstract lỗi (tham số sai, không có kết quả), agent bị kẹt hoặc thử lại nhiều lần thay vì tổng hợp thông tin từ kiến thức sẵn có.
        •	Tập trung quá hẹp: Agent chỉ tìm trên arXiv, không mở rộng sang dữ liệu cổ phiếu hay tóm tắt thị trường. Chatbot có thể đề xuất ý tưởng giao dịch thực tế ngay lập tức.
        •	Chậm hơn: Do ReAct suy nghĩ nhiều bước, agent đôi khi xử lý chậm và lặp lại, trong khi Chatbot trả lời liền mạch.

3.  **Observation**:
    Các phản hồi từ môi trường (observations) giúp agent:
        •	Xác nhận xem hành động trước có thành công hay không (ví dụ truy vấn arXiv trả về lỗi hay không có kết quả).
        •	Điều chỉnh bước tiếp theo: agent thay đổi truy vấn hoặc mở rộng phạm vi tìm kiếm dựa trên feedback.
        •	Học cách tránh lặp lại lỗi: nếu truy vấn quá hẹp, agent sẽ thử truy vấn rộng hơn hoặc thay đổi từ khóa.

    Tóm lại, observation giúp ReAct phản ứng linh hoạt, tạo ra luồng hành động có kiểm soát dựa trên kết quả thực tế.

## IV. Future Improvements (5 Points)

- **Scalability**: 
  + Sử dụng hàng đợi bất đồng bộ (asynchronous queue) cho các lần gọi tool, giúp agent xử + lý nhiều request song song mà không bị tắc.
  + Thiết kế kiến trúc microservice, mỗi tool là một service riêng, dễ thêm bớt và bảo trì.
- **Safety**: 
  + Triển khai Supervisor LLM để kiểm tra các hành động agent trước khi thực thi, tránh truy cập dữ liệu nhạy cảm hoặc hành vi sai lệch.
  + Giới hạn các action sandboxed: agent chỉ có thể thao tác với những công cụ và dữ liệu được phép.
- **Performance**: 
  + Dùng Vector Database để lưu trữ và truy xuất thông tin từ nhiều tool, tăng tốc độ tìm kiếm và kết nối dữ liệu.
  + Cache kết quả từ tool calls thường dùng, giảm số lần gọi lặp, tiết kiệm thời gian và chi phí.