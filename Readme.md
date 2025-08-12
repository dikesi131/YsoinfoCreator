# YsoinfoCreator

## Project Overview  
YsoinfoCreator is a graphical tool that automatically generates username and password dictionaries from personal information.

It is designed for authorized security research, penetration testing, and password-strength evaluation.

The application supports information collection, dictionary generation, result preview, database management, and export—all wrapped in a modern, user-friendly interface.

## Key Features  

- **Personal Information Collection**
  Accepts Chinese/English names, nicknames, birthdays, e-mail addresses, phone numbers, company/department, and more.  

- **Custom Rules**
  Add special characters, common suffixes, years, and other personalized rules to increase dictionary diversity.  

- **Dictionary Generation**
  High-quality usernames and passwords are generated via strategies such as pinyin, initials, and combinatorial mixing.  

- **Real-time Preview & Export**
  Instantly preview results and export them to plain-text files with one click.  

- **Database Management**
  Save tasks to a local SQLite database.
  Browse, search, inspect details, delete, and generate statistics for every task.  

- **Security Notice**
  Built-in warnings remind users to operate legally and ethically.  

- **Polished UI**
  High-contrast color scheme and card-style statistics ensure an intuitive experience.

## Installation & Run

### Requirements
- Python 3.8+  
- PyQt6  

### Install Dependencies
```sh
pip install PyQt6
```

### Start the Application
```sh
python YsoinfoCreator.py
```

## Usage Guide

1. **Fill in Personal Information**
   - Open the “Personal Information” tab and enter the required details.  
   - Data can be saved/loaded as JSON with built-in format validation.  

2. **Customize Rules**
   - Add special characters, suffixes, years, etc., to boost the dictionary’s variability.  

3. **Generate Dictionary**
   - Click “Generate Dictionary.”  
   - Progress bars and statistic cards update in real time.  

4. **Manage Results**
   - Preview the username & password lists.  
   - Copy, clear, or export to file.  
   - Optionally save the current result into the database.  

5. **Database Operations**
   - View historical tasks.  
   - Search, export, or delete tasks.  
   - Inspect task details and overall database statistics.  

6. **Security Reminders & Help**
   - Access security warnings and “About” information from the menu bar to ensure compliant usage.

## Workflow Demo

### Fill in Personal Information

![image-20250811234959979](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250811235006331.png) 

Enter the relevant data (name is mandatory; other fields optional). Click “Validate” to check the format.

### Generate Dictionary

![image-20250811235207540](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250811235207569.png) 

After all information is filled in, click “Generate Dictionary.” Preview the results and choose to save to **file** or **database** (database recommended).

### Load Information from Database or File

- **From Database**

(Requires existing saved records)

![image-20250812234602261](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250812234602348.png)  

Select a task and click “Load.”

![image-20250812234624475](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250812234624494.png)


All related dictionaries and personal information are retrieved.

- **From File**

![image-20250812234800069](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250812234800094.png)


After entering information, export it as JSON.

![image-20250812234919696](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250812234919725.png)


Re-import the JSON file later to reload the data and generate dictionaries.

### Export All Unique Results

![image-20250812235401789](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250812235401814.png)  
![image-20250812235150840](https://dikkksi-wiki-pic.oss-cn-chengdu.aliyuncs.com/wiki_img_2/20250812235150864.png)

To merge and deduplicate dictionaries from multiple tasks, click “Export All Unique Entries.”

## Project Structure

```
dic_toolkit/Social_engineering_dic_toolkit/
├── YsoinfoCreator.py         # Main GUI entry
├── main.py                   # Core business logic
├── core/                     # Business modules
├── gui_settings.py           # Global style settings
├── ...
```

## Notices

- This tool is **only** for authorized security testing and research—any illegal use is strictly prohibited.  
- Ensure you have explicit authorization from the target system owner before use.  
- The developer assumes **no liability** for misuse.

## License

MIT License