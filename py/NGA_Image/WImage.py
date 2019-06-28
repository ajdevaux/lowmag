import Tkinter as Tk
from PIL import Image, ImageTk
 

class NGA_WImage:

    fn = r"..\data\capture_py.png"
    fn_info = r"..\data\capture_py.txt"
    info = None
    img = None
    w = 0
    h = 0
    root = None
    
    def __init__(self):
        self.root = Tk.Toplevel() #.Tk()
        self.root.title(self.fn)

    def draw(self):
        self.load(self.fn)

    def load(self, fn):
        self.fn = fn
        self.root.title(self.fn)
        #self.img = ImageTk.PhotoImage(Image.open(r"../resources/nexgen_logo_80.png"))
        self.img = ImageTk.PhotoImage(Image.open(self.fn))
        # get the image size
        self.w = self.img.width()
        self.h = self.img.height()
        # position coordinates of root 'upper left corner'
        x = 0
        y = 0
        #print "%dx%d+%d+%d" % (self.w, self.h, x, y)         
        # make the root window the size of the image
        self.root.geometry("%dx%d+%d+%d" % (self.w, self.h, x, y))
         
        # root has no image argument, so use a label as a panel
        panel1 = Tk.Label(self.root, image=self.img)
        panel1.pack(side='top', fill='both', expand='yes')
         
        # put a button on the image panel to test it
        #button2 = Tk.Button(panel1, text='close', command=self.close_window)
        #button2.pack(side='top')
         
        # save the panel's image from 'garbage collection'
        panel1.image = self.img
         
        # start the event loop
        self.root.mainloop()

    def close_window(self):
        self.root.destroy()
