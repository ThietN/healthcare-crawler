import json
import pandas as pd
from bs4 import BeautifulSoup

# Read JSON file
with open("output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# List to store extracted data
output_data = []

# Process each entry in JSON
for item in data:
    title = item.get("title", "Unknown Disease")  # Get Disease Title
    html_content = item.get("content", "")  # Get HTML Content

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find <h2> Symptoms
    symptoms_section = soup.find("h2", text="Symptoms")

    symptoms_text = ""
    if symptoms_section:
        # Extract content until the next <h2>
        content = []
        for sibling in symptoms_section.find_next_siblings():
            if sibling.name == "h2":  # Stop when another <h2> appears
                break
            content.append(sibling.get_text(" ", strip=True))  # Clean text

        symptoms_text = " ".join(content)  # Combine text

    # Store the extracted data
    output_data.append([title, symptoms_text])

# Convert to DataFrame
df = pd.DataFrame(output_data, columns=["Disease", "Symptoms"])

# Save as Excel file
df.to_excel("output.xlsx", index=False)

print("✅ Done! Data saved as output.xlsx")
