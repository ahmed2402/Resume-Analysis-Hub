import google.generativeai as genai
import pandas as pd
import time
import os
from dotenv import load_dotenv

genai.configure(api_key="AIzaSyBgYU8uewGn8chN_T7uIZHSO3vbDXGNW38")
model = genai.GenerativeModel('gemini-2.5-flash')

categories = {
    'Web Developer': 30,
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
