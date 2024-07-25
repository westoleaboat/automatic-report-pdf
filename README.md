# Python Qt5 Automatic-report-PDF GUI
This program facilitates loggin of production data into a PDF
for automatic reporting

![Screenshot_select-area_20240725221928](https://github.com/user-attachments/assets/1a4451d1-1191-4448-99cd-03da24607d25)

## Requirements
Functional Requirements:

  * Provide a timer with Start, Stop, and Reset Buttons; 
    display of timer update when running.
  * Allow all relevant, valid data to be entered,
    as per the data dictionary.
  * automatically timestamp an input and log it onto screen 
    to follow production.
  * Append entered data to a PDF file:
    - The PDF file must have a filename of
    production_CURRENTDATE.pdf, where CURRENTDATE is the date
    of the production in ISO format (Year-month-day).
    - The PDF file must include all fields.
    listed in the data dictionary.
    - The PDF headers will avoid cryptic abbreviations.
  * Enforce correct datatypes per field.
  * have inputs that:
    - ignore meaningless keystrokes
    - display an error if the value is invalid on focusout
    - display an error if a required field is empty on focusout
  * prevent saving the record when errors are present

Non-functional Requirements:

  * Enforce reasonable limits on data entered, per the data dict.
  * Auto-fill data to save time.
  * Suggest likely correct values.
  * Provide a smooth and efficient workflow.
  * Store data in a format easily understandable by Python.

## TODO:
### Improvements
- [ ] improve layout design and details
- [ ] modify 'Check' column for better visual
- [ ] Add data validation
- [ ] Add more rows if necessary

### Completed
- [x] Update code logic
- [x] add timer
- [x] generate pdf
- [x] mvp minimum functionality

1. Clone this repo into a project folder and create a virtual environment
```
cd project-folder/
git clone https://github.com/westoleaboat/automatic-report-pdf.git
cd automatic-report-pdf/
python3 -m venv env_name
```

2. run report_maker.py 
```
python report_maker.py
```

