import json
import os

# Định nghĩa đường dẫn file JSON từ thư mục Downloads
file_path = r"E:\AI SC\2HM\2HM_Chatbot_Demo_New_Prompt.json"

# Kiểm tra file có tồn tại không
if not os.path.exists(file_path):
    print(f"❌ File not found: {file_path}")
    exit()

# Load n8n workflow JSON
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Kiểm tra dữ liệu hợp lệ
if "nodes" not in data or "connections" not in data:
    print("❌ Invalid n8n JSON format!")
    exit()

nodes = data["nodes"]
connections = data["connections"]

# Bắt đầu flowchart
mermaid_code = "graph TD;\n"

# Tạo danh sách nodes
node_ids = {node["id"]: node["name"] for node in nodes}
for node in nodes:
    mermaid_code += f'    {node["id"]}["{node["name"]}"];\n'

# Tạo danh sách connections
for source, targets in connections.items():
    if not isinstance(targets, list):
        print(f"⚠️ Skipping invalid targets for {source}: {targets}")
        continue

    for target in targets:
        if isinstance(target, dict) and "node" in target:
            mermaid_code += f'    {source} --> {target["node"]};\n'
        elif isinstance(target, list) and target and isinstance(target[0], dict) and "node" in target[0]:
            mermaid_code += f'    {source} --> {target[0]["node"]};\n'
        else:
            print(f"⚠️ Invalid target format: {target}")

# Xuất file Mermaid
output_file = r"E:\AI SC\2HM\workflow_diagram.mmd"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(mermaid_code)

print(f"✅ Mermaid file created: {output_file}")
