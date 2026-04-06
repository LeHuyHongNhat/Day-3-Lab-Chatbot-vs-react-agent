from src.tool.tool_definitions import execute_tool, get_available_tools

# Văn bản ví dụ để test
sample_text = """
Tiêu đề bài báo

Abstract: Bài báo này đề xuất một phương pháp mới để phân tích các metric AI. 
Chúng tôi đánh giá accuracy, F1 score và recall trên nhiều tập dữ liệu. 
Kết quả cho thấy cải thiện đáng kể.

Introduction: Lĩnh vực AI phát triển nhanh chóng...
"""

# 1. Xem danh sách các công cụ
tools = get_available_tools()
print("Danh sách các tool có sẵn:")
for t in tools:
    print("-", t['name'], ":", t['description'])

# 2. Test clean_text (làm sạch văn bản)
cleaned = execute_tool("clean_text", text=sample_text)
print("\n--- Văn bản đã làm sạch ---")
print(cleaned)

# 3. Test extract_abstract (trích Abstract)
abstract = execute_tool("extract_abstract", text=sample_text)
print("\n--- Abstract trích ra ---")
print(abstract)

# 4. Test extract_metadata (trích metadata)
metadata = execute_tool("extract_metadata", text=sample_text)
print("\n--- Metadata trích ra ---")
print(metadata)