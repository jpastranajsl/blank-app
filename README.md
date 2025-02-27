# 📊 Automated Financial Report Generator

Generate **professional** financial reports from CSV files, including:

✅ **Revenue & Expense breakdowns**  
✅ **Profit Trends**  
✅ **Custom PDF reports**  

## 🚀 Features
- Upload a **financial CSV file** or use a **Google Sheets template**.
- **Visualize revenue vs. expenses** in easy-to-read charts.
- **Download a structured PDF report** with financial insights.
- Simple **Streamlit UI** (no coding required for users).

---

## 🔧 Installation Guide

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
   ```

### 2️⃣ Run the App

   ```
   $ streamlit run app.py
   ```

## 📂 Files Overview
| File               | Description |
|--------------------|-------------|
| `app.py`          | The main Streamlit app that runs the project. |
| `sample_data.csv` | A sample financial CSV file for users to test. |
| `template.xlsx`   | An Excel template to fill up with financial records, later on has to be converted to CSV. |
| `requirements.txt` | Contains all dependencies required to run the app. |


## 📄 Google Sheets Template
If you prefer using Google Sheets, make a copy of this template to use:
🔗 [Google Sheets Template](https://docs.google.com/spreadsheets/d/1L0jB_Ak1wa4ZXR2SDn82f3fSQEhaaV1zmMp4ow8fI-c/edit?usp=sharing)

## 📸 Screenshots
This is how my app initially looks :D. 
<img width="1373" alt="Screenshot 2025-02-27 at 17 27 02" src="https://github.com/user-attachments/assets/3a7842b5-6f13-441a-8a95-4a0f2ca11f02" />

You simply have to upload a CSV file with the same structure seen as the sample_data.csv. You can either change the file format of the template.xlsx to CSV after filling it up, or make a copy of the Google Sheets template attached to this README and dowload it as a CSV file. After, you can put your business information on the sidebar, so this information can appear in the portrait of the PDF that will be generated.
<img width="1372" alt="Screenshot 2025-02-27 at 17 30 30" src="https://github.com/user-attachments/assets/74715bca-1c6c-42af-a34e-5cb54d334267" />
