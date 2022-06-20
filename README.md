# Python Tkinter Automatic-report-PDF GUI
create a report in PDF format automatically loggin your production info
![Screenshot_select-area_20220403021659](https://user-images.githubusercontent.com/68698872/174583729-9cd60f0f-bfcd-4b5e-9927-2fb89e3efd06.png)

1. Clone this repo into a project folder and create a virtual environment
```
cd project-folder/
git clone https://github.com/westoleaboat/automatic-report-pdf.git
cd automatic-report-pdf/
python3 -m venv env_name
```
2. install dependencies with pip
```
source env_name/bin/activate
pip install fpdf filestack-python
```
3. run brewlog.py (you may need sudo privileges to create a PDF in your project folder)
```
sudo python3 brewlog.py
```
4. start the timer before loggin your data. Click on 'Print report' to generate the PDF, a messagebox will indicate that the process was succesful.
