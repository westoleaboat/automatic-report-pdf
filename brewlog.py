#from tkinter import Tk, Label
from tkinter import *
from tkinter import messagebox
from datetime import time
from fpdf import FPDF
from filestack import Client
#import qrcode

from datetime import date, datetime, timedelta

# timer parameters
running = False
counter = 0

class Content:
    def __init__(self, root):


        def stopwatch():
            global count

            def count():
                if running:
                    global counter, display, string, dt

                    if counter == 0:
                        display = 'Starting'
                    else:
                        seconds = counter % 60
                        minutes = (counter // 60) % 60
                        hours = (counter // (60 * 60)) % (60 * 60)

                        dt = time(second=seconds, minute=minutes, hour=hours)
                        string = dt.isoformat(timespec= 'auto')
                        display = string
                    lbl['text']=display
                    counter += 1
                root.after(100, count) # use 1000 for 1 second time
            count()

        def sw_start():
            global running
            running = True

        def sw_stop():
            global running
            running = False

        def sw_reset():
            global counter
            response=messagebox.askquestion("Confirm Timer Reset", "Are you sure you want to reset the timer?")
            if response == "yes":
                counter = 0
                if running == False:
                    lbl['text']='00:00:00'
                else:
                    lbl['text']='Starting'
            else:
                pass

        

        def comment():
            global display
            value = log_input.get("1.0", "end-1c")
            log_text['state']='normal'
            if value == "":
                pass
            else:
                #tt = dt.isoformat(timespec= 'auto')
                try:
                    log_input.delete("1.0", "end")
                    text_to_add = (display + "|" + "\t" + value + "\n")
                    log_text.insert(END, text_to_add)
                except NameError:
                    messagebox.showinfo("Atention!", "Start the timer before adding a comment")
            log_text['state']='disabled'

        #def qr_code():
            #data = 'www.somelink.com'
            #image_qr = qrcode.make(data)
            #image_qr.save('report1qrcode.png')
            #return image_qr

        def print_report():
            #pass
            text_to_print = log_text.get("1.0", "end-1c")
            if text_to_print == '':
                pass
            else:
                global image_qr
                #doc = FPDF()
                #qr_code()
                doc=FPDF(orientation="P", unit='pt', format='A4')
                doc.add_page()
                doc.set_font("Arial", size=15)
                doc.cell(w=100, h=80, txt='Company logo', border=1, align='C')
                doc.cell(w=100, h=80, txt='## This report has been autogenerated ##', align='L', ln=1)
                #doc.image('report1qrcode.png', x=450, y=32.5, w=80, h=80)
                doc.multi_cell(350, 20, txt=text_to_print, align="L") # ln=1,
                doc.output("pdf_file_sample.pdf")
                #print('Your PDF has been created as "pdf_file_sample.pdf" ')
                
                
                #Filestack share file online
                client=Client('AM9fqJoiDQ5Cf5ktFB4e9z')
                new_filelink=client.upload(filepath='pdf_file_sample.pdf')
                messagebox.showinfo("PDF", f"your PDF has been created as \"pdf_file_sample.pdf\"\nShare it with {new_filelink.url} ")
                print('Visit the following URL to acces your report from anywhere:\n{}'.format(new_filelink.url))

        # create PDF button
        print_btn = Button(text='print report', command=print_report)
        print_btn.place(x=10, y=10)

        # log commented text button
        comment_btn = Button(text='comment', 
                height=5, width=50, command=lambda:comment())
        comment_btn.place(x=450, y=280)

        # input text container
        lf_in = LabelFrame(text='INPUT', font='verdana 15')
        lf_in.place(x=450, y=90)

        # input text widget
        log_input = Text(lf_in, height=10, width=60)
        log_input.pack()
        
        # log text container
        lf_out = LabelFrame(text='LOG', font='Verdana 15')
        lf_out.place(x=10, y=90)


        # logged text widget
        log_text = Text(lf_out, height=20, width=30, font='Verdana 15')
        log_text['state']='disabled'
        log_text.pack()

        # recipe text container
        lf_recipe_info = LabelFrame(text='RECIPE', font='Verdana 15',)
        lf_recipe_info.place(x=450, y=390)

        # recipe text widget
        recipe_lbl = Label(lf_recipe_info, text='Sample recipe text', 
                height=10, width=50).pack()

        display_lf = LabelFrame(bg='#ffffff')
        display_lf.pack()

        lbl = Label(display_lf, text='00:00:00', font='Verdana 20', bg='#ffffff')
        lbl.pack()

        btn_start = Button(display_lf, text='Start', command=sw_start)
        btn_start.pack(side='left')

        btn_stop = Button(display_lf, text='Stop', command=sw_stop)
        btn_stop.pack(side='left')

        btn_reset = Button(display_lf, text='Reset', command=sw_reset)
        btn_reset.pack(side='left')

        stopwatch()


def main():
    root = Tk()
    cnt = Content(root)
    root.geometry('900x640+300+50') # width, height, left, top
    root.resizable(0,0)
    root.mainloop()

if __name__ == '__main__':
    main()



