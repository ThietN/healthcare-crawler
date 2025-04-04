import re
import json
import csv

# Regular expression pattern to extract symptoms
pattern = r'has_symptom([\w\s]+?)(?=,|\.|and|or)'


# Function to read OBO file & extract terms
def read_obo(path) -> list:
    entries = []
    try:
        with open(path, encoding='utf-8') as fp:
            for line in fp:
                if '[Term]' not in line:
                    continue
                entry = {}
                while True:
                    line = next(fp, "").strip()
                    if not line:
                        break
                    key_value = line.split(':', 1)
                    if len(key_value) != 2:
                        continue
                    key, value = key_value
                    value = value.strip()

                    if key == 'def':  # Find all symptom matches
                        symptoms = re.findall(pattern, value)
                        if symptoms:
                            entry.setdefault('symptom', []).extend(s.strip() for s in symptoms)
                        continue

                    if key == 'synonym':  # Add synonyms to the name list
                        entry.setdefault('name', []).append(value)
                        continue

                    entry.setdefault(key, []).append(value)

                entries.append(entry)
    except Exception as e:
        print(f"Error reading OBO file ({path}): {e}")
    return entries


# Function to read JSON file
def open_output_mayo(path):
    try:
        with open(path, encoding="utf-8") as fp:
            return json.load(fp)
    except Exception as e:
        print(f"Error reading JSON file ({path}): {e}")
        return []


# Map symptoms to diseases
def map_symp_disease(mayo_data, symps_obo) -> list:
    mapped_data = []
    for disease in mayo_data:
        disease_name = disease.get('title', 'Unknown Disease')
        symptoms_list = disease.get('symptoms', '').lower()

        disease_symp = {disease_name: []}
        for symp in symps_obo:
            for name in symp.get('name', []):
                if name.lower() in symptoms_list and name.lower() != 'symptom':
                    disease_symp[disease_name].append(name.lower())
                    break
        mapped_data.append(disease_symp)

    return mapped_data


# Add DOID ID, symptoms, and is_a mappings
def map_symp_disease_doid(symp_disease, doid_obo):
    for doid_term in doid_obo:
        matched = False
        for name in doid_term.get('name', []):
            for disease in symp_disease:
                if next(iter(disease.keys())).lower() == name.lower():
                    matched = True
                    disease[next(iter(disease.keys()))] = list(
                        set(disease[next(iter(disease.keys()))] + doid_term.get('symptom', [])))
                    disease.setdefault('id', []).append(doid_term.get('id', ['Unknown'])[0])
                    disease.setdefault('is_a', []).extend(doid_term.get('is_a', []))
                    break
            if matched:
                break
        if not matched:
            new_disease = {doid_term.get('name', ['Unknown'])[0]: doid_term.get('symptom', [])}
            new_disease['id'] = doid_term.get('id', ['Unknown'])
            new_disease['is_a'] = doid_term.get('is_a', [])
            symp_disease.append(new_disease)
    return symp_disease


# Add symptom ID mappings
def map_symp_disease_doid_symp(symp_disease_doid, symps_obo) -> list:
    for disease in symp_disease_doid:
        symptoms = next(iter(disease.values()), [])
        for i, symptom in enumerate(symptoms):
            for symp_obo in symps_obo:
                if symptom.rstrip('s') in [s.rstrip('s') for s in symp_obo.get('name', [])]:
                    disease[next(iter(disease.keys()))][i] = f"{symptom} SYMP:{symp_obo.get('id', ['Unknown'])[0]}"
    return symp_disease_doid


# Save data to CSV
def save_to_csv(symp_disease_doid_symp):
    try:
        with open('csv_output.csv', 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Disease', 'DOIDId', 'Symptom', 'SymptomId'])

            for entry in symp_disease_doid_symp:
                disease_name = list(entry.keys())[0]
                disease_id = entry.get("id", ["Unknown"])[0]
                symptoms = entry[disease_name]

                for symptom in symptoms:
                    if "SYMP:" in symptom:
                        symptom_name, symptom_code = symptom.split("SYMP:")
                        writer.writerow(
                            [disease_name, disease_id, symptom_name.strip(), f'SYMP:{symptom_code.strip()}'])

                for is_a in entry.get('is_a', []):
                    writer.writerow([disease_name, disease_id, 'is_a', is_a.split('!')[0].strip()])

        print("✅ CSV output saved successfully: csv_output.csv")
    except Exception as e:
        print(f"Error writing CSV file: {e}")


# Main function
def main():
    print("📂 Loading JSON and OBO files...")
    mayo_data = open_output_mayo('./output-symps.json')
    doid_obo = read_obo('./doid.obo')
    symps_obo = read_obo('./symp.obo')

    print("🔍 Mapping symptoms to diseases...")
    results_map_symp_disease = map_symp_disease(mayo_data, symps_obo)

    print("🔄 Mapping DOID and additional disease info...")
    results_map_symp_disease_doid = map_symp_disease_doid(results_map_symp_disease, doid_obo)

    print("📌 Adding symptom IDs...")
    result_map_symp_disease_doid_symp = map_symp_disease_doid_symp(results_map_symp_disease_doid, symps_obo)

    print("💾 Saving JSON outputs for debugging...")
    with open('symp_mayo_map.json', 'w', encoding="utf-8") as jf:
        json.dump(results_map_symp_disease, jf, ensure_ascii=False, indent=4)

    with open('doid_symp_mayo_map.json', 'w', encoding="utf-8") as jf:
        json.dump(results_map_symp_disease_doid, jf, ensure_ascii=False, indent=4)

    with open('doid_symp_mayo_sympID_map.json', 'w', encoding="utf-8") as jf:
        json.dump(result_map_symp_disease_doid_symp, jf, ensure_ascii=False, indent=4)

    print("📊 Saving final CSV...")
    save_to_csv(result_map_symp_disease_doid_symp)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
