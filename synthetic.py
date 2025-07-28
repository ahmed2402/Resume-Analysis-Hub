import google.generativeai as genai
import pandas as pd
import time
import os
from dotenv import load_dotenv

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

categories = {
    "Java Developer": 20,
    "Database": 20,
    "Advocate": 20,
    "HR": 20,
    "Data Science": 20,
    "Automation Testing": 20,
    "DevOps Engineer": 20,
    "Testing": 20,
    "DotNet Developer": 20,
    "Hadoop": 20,
    "SAP Developer": 20,
    "Python Developer": 20,
    "Health and fitness": 20,
    "Civil Engineer": 20,
    "Arts": 20,
    "Business Analyst": 20,
    "Sales": 20,
    "Blockchain": 20,
    "Mechanical Engineer": 20,
    "ETL Developer": 20,
    "Electrical Engineering": 20,
    "Network Security Engineer": 20,
    "Web Designing": 20,
    "Operations Manager": 20,
    "PMO": 20
}

def generate_resumes(category, count=20):
    prompt = f"""Generate {count} synthetic resume texts for the job category '{category}'.
Each resume should be 4-5 lines long, sound realistic and unique, and include:
- A job title
- Key skills
- Short experience description
- Tools or technologies used
Output them as a numbered list."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Error for category '{category}': {e}")
        return ""

def parse_resumes_to_df(response_text, category):
    lines = response_text.strip().split('\n')
    data = []
    current_resume = ""
    for line in lines:
        if line.strip().startswith(tuple(f"{i}." for i in range(1, 200))):
            if current_resume:
                data.append(current_resume.strip())
            current_resume = line.split('.', 1)[1].strip()
        else:
            current_resume += ' ' + line.strip()
    if current_resume:
        data.append(current_resume.strip())
    df = pd.DataFrame({'Resume': data[:len(data)], 'Category': category})
    return df

all_data = []

for category, count in categories.items():
    print(f"🌀 Generating resumes for: {category} ({count})")
    response_text = generate_resumes(category, count)
    if response_text:
        df = parse_resumes_to_df(response_text, category)
        all_data.append(df)
        print(f"✅ Collected {len(df)} resumes for {category}")
    else:
        print(f"⚠️ Skipped {category} due to error.")
    time.sleep(2)

final_df = pd.concat(all_data, ignore_index=True)
print(f"\n🎉 Total resumes generated: {len(final_df)}")

final_df.to_csv("synthetic_resume_dataset.csv", index=False)
print("✅ Saved to 'synthetic_resume_dataset.csv'")
