import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps
from AridBuddy import Model

class MyChatbot(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        c_x = int(width/2-800/2)
        c_y = int(height/2-600/2)
        self.title("Arid Buddy")
        self.geometry(f"800x600+{c_x}+{c_y-30}")
        self.resizable(False, False)
        self.iconbitmap("data/images/logoIcon.ico")
        self.mainpage()
        self.model = Model()
        
    def mainpage(self):
        
        # Opening the required Images
        Aridlogo = ctk.CTkImage(light_image=(Image.open("data/images/buddy.png")), size=(150, 150))
        sendlogo = ctk.CTkImage(light_image=(Image.open("data/images/send.png")), size=(30, 30))
        deletelogo = ctk.CTkImage(light_image=(Image.open("data/images/delete.png")), size=(20, 20))
        
        
        self.sideFrame = ctk.CTkFrame(self, width=200, height=600, fg_color="#b6d0be", corner_radius=0,
                         border_width=2, border_color="#000000")
        self.sideFrame.place(relx=0, rely=0, anchor="nw")
        
        self.mainframe = ctk.CTkFrame(self, width=600, height=600, fg_color="#ffffff", corner_radius=0,
                         border_width=2, border_color="#000000")
        self.mainframe.place(relx=0.25, rely=0, anchor="nw")
        
        self.chatframe = ctk.CTkFrame(self.mainframe, width=600, height=600, fg_color="#ffffff", corner_radius=0,
                         border_width=2, border_color="#000000")
        self.chatframe.place(relx=0, rely=0, anchor="nw")
        
        self.messageframe = ctk.CTkScrollableFrame(self.chatframe, width=580, height=480, fg_color="#ffffff",
                         corner_radius=0)
        self.messageframe.place(relx=0.5, rely=0.5, anchor="center")
        
        self.messageframe.grid_columnconfigure(0, weight=1)
        self.messageframe.grid_columnconfigure(1, weight=1)
        
        self.logoLabel = ctk.CTkLabel(self.sideFrame, width=150, height=150, text="", image=Aridlogo)
        self.logoLabel.place(x=20, y=10)
        
        self.titleLabel = ctk.CTkLabel(self.chatframe, width=550, height=50, text="Arid Buddy: Your AI Companion",
                           font=("Roboto", 30, "bold"), text_color="#085928")
        self.titleLabel.place(x=300, y=30, anchor="center")
                
        self.messagebox = ctk.CTkTextbox(self.chatframe, width=520, height=40, border_color="#000000",
                         wrap="word", font=("Arial", 14), border_width=2, fg_color="#ffffff", 
                         text_color="#000000", corner_radius=10)
        self.messagebox.place(relx=0.47, rely=0.95, anchor="center")
        
        self.sendBtn = ctk.CTkButton(self.chatframe, width=30, height=30, text="", image=sendlogo,
                        corner_radius=10, fg_color="#ffffff", hover=False, cursor="hand2",
                        command=self.send_message)
        self.sendBtn.place(relx=0.95,rely=0.95,anchor="center")
        
        self.messagebox.insert("0.0", "Enter Your Message")
        
        self.messagebox.bind("<FocusIn>", self.clear_placeholder)
        self.messagebox.bind("<FocusOut>", self.add_placeholder)
        self.messagebox.bind("<Return>", self.send_message)
        
        self.new_chatBtn = ctk.CTkButton(self.sideFrame, width=130, height=30, text="Clear Chat",
                             fg_color="#085928", text_color="#ffffff", font=("Roboto", 18, "bold"),
                             hover=False, cursor="hand2", corner_radius=20, command=self.new_chat)
        self.new_chatBtn.place(x=25, y=200)
        
        self.aboutBtn = ctk.CTkButton(self.sideFrame, width=130, height=30, text="About us",
                             fg_color="#085928", text_color="#ffffff", font=("Roboto", 18, "bold"),
                             hover=False, cursor="hand2", corner_radius=20, command=self.about_page)
        self.aboutBtn.place(x=25, y=250)
    
    def add_placeholder(self, event):       
        if self.messagebox.get("0.0", "end").strip() == "":
            self.messagebox.insert("0.0", "Enter Your Message")
            
    def clear_placeholder(self, event):
        if self.messagebox.get("0.0", "end").strip() == "Enter Your Message":
            self.messagebox.delete("0.0", "end")
    
    def send_message(self, event=None):
        user_message = self.messagebox.get("0.0", "end").strip()
        
        if user_message != "Enter Your Message" and user_message != "":
            self.messagebox.delete("0.0", "end")
            self.display_message(user_message, side="left")
            
            bot_response = self.get_bot_response(user_message)
            self.display_message(bot_response, side="right")
    
    def display_message(self, message ,side):
        self.messageLabel = ctk.CTkLabel(self.messageframe, text=message, wraplength=300, corner_radius=10, 
                            fg_color="#006400" if side == "right" else "#d0f0c0", 
                            text_color="#000000" if side == "left" else "#ffffff",
                            font=("Arial", 12))
        
        if side == "left":
            self.messageLabel.grid(row=self.get_row(), column=0, sticky="w")
        else:
            self.messageLabel.grid(row=self.get_row(), column=1, sticky="e")
    
    def get_row(self):        
        return len(self.messageframe.winfo_children())
    
    def get_bot_response(self, user_message):
            ints = self.model.predict_class(user_message)
            res = self.model.get_response(ints, self.model.intents)
            return res
        
    def new_chat(self):
        for widget in self.messageframe.winfo_children():
            widget.destroy()
            
    def back_button(self):
        self.aboutFrame.destroy()
        # self.chatframe.place(relx=0, rely=0, anchor="nw")
        self.new_chatBtn.configure(state="normal")
        self.mainpage()
    
    def make_round(self, img_path, size=(150, 150)):
        img = Image.open(img_path).resize(size)
        
        mask = Image.new('L', img.size, 0)
        draw = ImageDraw.Draw(mask)
        
        draw.ellipse((0,0) + img.size, fill=255)
        
        img = ImageOps.fit(img, mask.size, centering=(0.5,0.5))
        img.putalpha(mask)
        
        return img
    
    def about_page(self):
        self.chatframe.place_forget()
        self.new_chatBtn.configure(state="disabled")
        
        team1 = self.make_round("data/Team Members/Amanullah.jpg")
        team2 = self.make_round("data/Team Members/Tayyab.jpg")
        team3 = self.make_round("data/Team Members/Zeeshan.jpg")
        
        team1_image = ctk.CTkImage(light_image=team1, size=(150, 150))
        team2_image = ctk.CTkImage(light_image=team2, size=(150, 150))
        team3_image = ctk.CTkImage(light_image=team3, size=(150, 150))
        
        back = ctk.CTkImage(light_image=(Image.open("data/images/back.png")), size=(30,30))
        
        
        self.aboutFrame = ctk.CTkScrollableFrame(self.mainframe, width=600, height=600, fg_color="#ffffff",
                            border_color="#000000", border_width=2, corner_radius=0)
        self.aboutFrame.place(relx=0, rely=0, anchor="nw")

        team1_frame = ctk.CTkFrame(self.aboutFrame, fg_color="#ffffff")
        team2_frame = ctk.CTkFrame(self.aboutFrame, fg_color="#ffffff")
        team3_frame = ctk.CTkFrame(self.aboutFrame, fg_color="#ffffff")
        
        self.backBtn = ctk.CTkButton(self.aboutFrame, width=30, height=30, hover=False, cursor="hand2", text="", image=back, 
                                     command=self.back_button, fg_color="#ffffff")
        self.backBtn.place(x=0, y=0)
        
        self.heading_label = ctk.CTkLabel(self.aboutFrame, text="Our Journey", font=("Arial", 30, "bold"), text_color="#1b5b85")
        self.heading_label.pack(pady=10)

        intro_label = ctk.CTkLabel(self.aboutFrame, text="Introduction", font=("Arial", 20, "bold"), text_color="#000000")
        intro_label.pack(padx=(10, 5), pady=(10, 5), anchor="w")

        intro_text = "Welcome to Arid Buddy! This innovative project is designed to assist users in navigating the complexities of their academic and personal journeys. " \
                    "Created to serve as a reliable companion for students at Arid Agriculture University.Arid Buddy aims to empower students with the tools needed for success while providing an enjoyable and engaging experience."
        intro_paragraph = ctk.CTkLabel(self.aboutFrame, text=intro_text, font=("Arial", 12), text_color="#000000", wraplength=580, justify="left")
        intro_paragraph.pack(pady=(0, 10))

        tech_section_heading = ctk.CTkLabel(self.aboutFrame, text="Technologies Used", font=("Arial", 20, "bold"), text_color="#000000")
        tech_section_heading.pack(padx=(10, 0), pady=(10, 5), anchor="w")

        nlp_label = ctk.CTkLabel(self.aboutFrame, text="Natural Language Processing (NLP)", font=("Arial", 16, "bold"), text_color="#000000")
        nlp_label.pack(padx=(25, 0), pady=(5, 0), anchor="w")
        nlp_description = ctk.CTkLabel(self.aboutFrame, text="The application employs NLP to understand and respond to user queries effectively.", font=("Arial", 12), text_color="#000000", wraplength=580, justify="left")
        nlp_description.pack(padx=(15, 0), pady=(0, 0))

        discriminative_model_label = ctk.CTkLabel(self.aboutFrame, text="Discriminative Model", font=("Arial", 16, "bold"), text_color="#000000")
        discriminative_model_label.pack(padx=(25, 0), pady=(5, 0), anchor="w")
        discriminative_model_description = ctk.CTkLabel(self.aboutFrame, text="A discriminative model  has been implemented to accurately classify user intents.", font=("Arial", 12), text_color="#000000", wraplength=580, justify="left")
        discriminative_model_description.pack(padx=(20, 0), pady=(0, 0))

        machine_learning_label = ctk.CTkLabel(self.aboutFrame, text="Deep Learning", font=("Arial", 16, "bold"), text_color="#000000")
        machine_learning_label.pack(padx=(25, 0), pady=(5, 0), anchor="w")
        machine_learning_description = ctk.CTkLabel(self.aboutFrame, text="Fully Connected Neural Network has been employed to enhance predictive capabilities.", font=("Arial", 12), text_color="#000000", wraplength=580, justify="left")
        machine_learning_description.pack(padx=(25, 0), pady=(0, 0))

        responsive_design_label = ctk.CTkLabel(self.aboutFrame, text="Responsive Design", font=("Arial", 16, "bold"), text_color="#000000")
        responsive_design_label.pack(padx=(25, 0), pady=(5, 0), anchor="w")
        responsive_design_description = ctk.CTkLabel(self.aboutFrame, text="The application features a responsive design, making it accessible on windows.", font=("Arial", 12), text_color="#000000", wraplength=580, justify="left")
        responsive_design_description.pack(padx=(25, 0), pady=(0, 0))

        team_label = ctk.CTkLabel(self.aboutFrame, text="Team Members", font=("Arial", 20, "bold"), text_color="#000000")
        team_label.pack(padx=(10, 0), pady=(10, 5), anchor="w")

        team_member1_photo = ctk.CTkLabel(team1_frame, text="", width=150, height=150, image=team1_image)
        team_member1_photo.pack(side="top")

        team_member2_photo = ctk.CTkLabel(team2_frame, text="", width=150, height=150, image=team2_image)
        team_member2_photo.pack(side="top")
        
        team_member3_photo = ctk.CTkLabel(team3_frame, text="", width=150, height=150, image=team3_image)
        team_member3_photo.pack(side="top")

        team_member1 = ctk.CTkLabel(team1_frame, text="Amanullah", font=("Arial", 16, "bold"), text_color="#1b5b85")
        team_member1.pack(side="bottom")

        team_member2 = ctk.CTkLabel(team2_frame, text="Tayyab", font=("Arial", 16, "bold"), text_color="#1b5b85")
        team_member2.pack(side="bottom")
        
        team_member3 = ctk.CTkLabel(team3_frame, text="Zeeshan", font=("Arial", 16, "bold"), text_color="#1b5b85")
        team_member3.pack(side="bottom")
        
        team1_frame.pack(side="left", padx=(40,0), pady=(0, 10))
        team3_frame.pack(side="left", padx=(50,0), pady=(0, 10))
        team2_frame.pack(side="left", padx=(50,0), pady=(0, 10))

if __name__ == "__main__":
    app = MyChatbot()
    app.mainloop()
    