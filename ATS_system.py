
!pip install pandas
!pip install os
!pip install pdfplumber
!pip install numpy
!pip install docx2txt
import os
import pandas as pd
import numpy
import pdfplumber
import docx2txt

path = "/home"
file_list = os.listdir(path)
print(type(file_list))
print(len(file_list))

path = "/home"
file_name = os.listdir(path)
print("Number of Resume:", len(file_name))
print("filenames (First 5 resumes):")
print(file_name[:5])

file_extension = []
for file_name in os.listdir(path):
  file_extension.append(os.path.splitext(file_name)[-1])
print(set(file_extension))

from collections import Counter
file_extension_count = Counter (file_extension)
print(file_extension_count)
print()
print("file extensions and count:")
for ext, cnt in file_extension_count.items():
  print(f"{ext} :{cnt}")

def extract_text_docx(file_path):
    text =docx2txt.process(file_path)
    return text
def extact_text_pdf(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
      for page in pdf.pages:
          text += page.extract_text()
    return text

import os
import pandas as pd

path = '/home'

df = pd.DataFrame(columns=['file_name', 'text'])

# Iterate over all files in the specified directory
for file_name in os.listdir(path):
    file_path = os.path.join(path, file_name)  # Correct path handling
    text = ''

    if file_name.endswith(".pdf") or file_name.endswith(".PDF"):
        try:
            text = extact_text_pdf(file_path)  # Corrected function name
        except Exception as e:
            print(f"PDF Error For: {file_path}, {e}")

    if file_name.endswith(".docx"):
        try:
            text = extract_text_docx(file_path)  # Corrected function name
        except Exception as e:
            print(f"DOCX Error For: {file_path}, {e}")

    if text:
        df.loc[len(df)] = [file_name, text]


print(df.head())

import re

email_pattern = r'[a-zA-Z0-9,_%+-]+@[a-zA-Z0-9.-]+\-[a-zA-Z]{2,}'
phone_pattern = r'\+?\d[\d J*{8,13}\d'
def extract_email(content):
    email = re.findall(email_pattern, content)
    return email
def extract_phone(content):
    phone = re.findall(phone_pattern, content)
    return phone

df['emails'] = df['text'].apply(lambda x: extract_email(x))
df['phone_numbers'] = df['text'].apply(lambda x: extract_phone(x))
df.head()

email_pattern = r'[a-zA-Z0-9,_%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
phone_pattern = r'\+?\d[\d -]{8,13}\d'  # Updated phone pattern
linkedin_pattern = r'www\.linkedin\.com/in/[a-zA-Z0-9-]+'
def extract_email(content):
    email = re.findall(email_pattern, content)
    return email
def extract_phone(content):
    phone = re.findall(phone_pattern, content)
    return phone
def extract_linkdin(content):
    linkdin = re.findall(linkedin_pattern, content)
    return linkdin

df['emails'] = df['text'].apply(lambda x: extract_email(x))
df['phone_numbers'] = df['text'].apply(lambda x: extract_phone(x))
df['linkdin_id'] = df['text'].apply(lambda x: extract_linkdin(x))
df.head()

skillset_score = {  'python': 2,
                   'NGS': 3,
                     'Bash': 3,
                     'MD': 2,
                     'Devolopment system':2,
                     'R programming': 2,
                     'SQL': 1,

                 }
 skillset_score.keys()

import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)

regex = '(' + '|'.join(skillset_score.keys()) + ')'
regex
'(Python| NGS | Development system| R programming | SQL | MD | Bash ) '

def extract_skill(content):
    skills = re.findall(regex,content.lower())
    skills = re.findall(regex,content.upper()) # Assuming you want to use the same regex here
    return skills

import re

def extract_skill(content):
    # Extract skills from lowercase content
    skills_lower = re.findall(regex, content.lower(), re.IGNORECASE)

    # Extract skills from uppercase content
    skills_upper = re.findall(regex, content.upper(), re.IGNORECASE)

    # Combine and remove duplicates
    all_skills = skills_lower + skills_upper
    unique_skills = list(set(all_skills))

    return unique_skills

df['skillset'] = df['text'].apply(lambda x : extract_skill(x))
df.head()

df['skillset'] = df['skillset'].apply(lambda x : list(set(x)))
df.head()


df_skills = df.explode('skillset')
df_skills.head()

df_skills['skillset_score'] = df_skills['skillset'].apply(lambda x: skillset_score.get(x, 0))
df_skills.head(20)

group_df= df_skills.groupby('file_name')
group_df['skillset_score'].sum()

profile_scores = group_df['skillset_score'].sum()
profile_scores.head()

sorted_profile_scores = profile_scores.sort_values(ascending=False)
sorted_profile_scores

# Filter the top profiles
sorted_profile_scores[sorted_profile_scores >= 6]



import numpy as np
import IPython.display as display
from matplotlib import pyplot as plt
import io
import base64

ys = 200 + np.random.randn(100)
x = [x for x in range(len(ys))]

fig = plt.figure(figsize=(4, 3), facecolor='w')
plt.plot(x, ys, '-')
plt.fill_between(x, ys, 195, where=(ys > 195), facecolor='g', alpha=0.6)
plt.title("Sample Visualization", fontsize=10)

data = io.BytesIO()
plt.savefig(data)
image = F"data:image/png;base64,{base64.b64encode(data.getvalue()).decode()}"
alt = "Sample Visualization"
display.display(display.Markdown(F"""![{alt}]({image})"""))
plt.close(fig)

