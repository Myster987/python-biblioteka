import customtkinter as ctk
from tkinter import messagebox
from biblioteka_baza_danych import DataBase, User


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SignUpScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sign Up")

        self.window_width = 270
        self.window_height = 330

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        if app.cords[0] is None:
            app.cords = ((self.screen_width // 2) - (self.window_width // 2), (self.screen_height // 2) - (self.window_height // 2))

        self.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)

        self.welcome_text_label = ctk.CTkLabel(self, text="Welcome!", font=("Roboto", 25, "bold"))
        self.welcome_text_label.grid(row=0, column=0, padx=20, pady=(10, 0), columnspan=2)

        self.info_text_label = ctk.CTkLabel(self, text="Please create your account", font=("Roboto", 15), text_color="gray")
        self.info_text_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="n")

        self.user_email_entry = ctk.CTkEntry(self, placeholder_text="Enter your email", placeholder_text_color="silver", font=("Roboto", 20))
        self.user_email_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.user_password_entry = ctk.CTkEntry(self, placeholder_text="Enter your password", placeholder_text_color="silver", font=("Roboto", 20))
        self.user_password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.sign_up_button = ctk.CTkButton(self, text="Sign Up", font=("Roboto", 32), command=self._sign_up)
        self.sign_up_button.grid(row=4, column=0, columnspan=2, padx=10, pady=(55, 5), sticky="we")

        self.to_sign_in_page_button = ctk.CTkButton(self, text="Already Have An Account? Sign In", font=("Roboto", 15), fg_color="transparent", command=app.show_sign_in_screen)
        self.to_sign_in_page_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="s")

    def _clear_entries(self):
        self.user_email_entry.delete(0, ctk.END)
        self.user_password_entry.delete(0, ctk.END)

    def _sign_up(self):
        email = self.user_email_entry.get()
        password = self.user_password_entry.get()

        if "@" not in email: 
            self.user_email_entry.delete(0, ctk.END)
            self.user_email_entry.configure(placeholder_text="Enter email domain!")
            self.focus() 
            return
        if len(email) < 11: 
            self.user_email_entry.delete(0, ctk.END)
            self.user_email_entry.configure(placeholder_text="Email is too short!")
            self.focus() 
            return
        if len(password.replace(" ", "")) < 4: 
            self.user_password_entry.delete(0, ctk.END)
            self.user_password_entry.configure(placeholder_text="Password is too short!")
            self.focus() 
            return

        res = app.db.add_user(email, password)
        if res:
            self._clear_entries()
            user = app.db.return_user_data(email, password)
            app.show_user_screen(user)
        else:
            messagebox.showinfo(title="Error", message="This email is already registered.\nPlease enter new one")

    def return_postion_of_window(self):
        return (self.winfo_x(), self.winfo_y())
    
    def set_new_postion_of_window(self):
        self.geometry(f"{self.window_width}x{self.window_height}+{app.cords[0]}+{app.cords[1]}")

class SignInScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sign In")

        self.window_width = 270
        self.window_height = 330

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        if app.cords[0] is None:
            app.cords = ((self.screen_width // 2) - (self.window_width // 2), (self.screen_height // 2) - (self.window_height // 2))

        self.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)


        self.welcome_text_label = ctk.CTkLabel(self, text="Welcome Back!", font=("Roboto", 25, "bold"))
        self.welcome_text_label.grid(row=0, column=0, padx=20, pady=(10, 0), columnspan=2)

        self.info_text_label = ctk.CTkLabel(self, text="Please sign in to your account", font=("Roboto", 15), text_color="gray")
        self.info_text_label.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="n")

        self.user_email_entry = ctk.CTkEntry(self, placeholder_text="Enter your email", placeholder_text_color="silver", font=("Roboto", 20))
        self.user_email_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.user_password_entry = ctk.CTkEntry(self, placeholder_text="Enter your password", placeholder_text_color="silver", font=("Roboto", 20))
        self.user_password_entry.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        self.sign_in_button = ctk.CTkButton(self, text="Sign In", font=("Roboto", 32), command=self._sign_in)
        self.sign_in_button.grid(row=4, column=0, columnspan=2, padx=10, pady=(55, 5), sticky="we")

        self.to_sign_up_page_button = ctk.CTkButton(self, text="Don't Have An Account? Sign Up", font=("Roboto", 15), fg_color="transparent", command=app.show_sign_up_screen)
        self.to_sign_up_page_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="s")

    def _clear_entries(self):
        self.user_email_entry.delete(0, ctk.END)
        self.user_password_entry.delete(0, ctk.END)

    def _sign_in(self):
        email = self.user_email_entry.get()
        password = self.user_password_entry.get()

        if "@" not in email: 
            self.user_email_entry.delete(0, ctk.END)
            self.user_email_entry.configure(placeholder_text="Enter email domain!")
            self.focus() 
            return
        if len(email) < 11: 
            self.user_email_entry.delete(0, ctk.END)
            self.user_email_entry.configure(placeholder_text="Email is too short!")
            self.focus() 
            return
        if len(password.replace(" ", "")) < 4: 
            self.user_password_entry.delete(0, ctk.END)
            self.user_password_entry.configure(placeholder_text="Password is too short!")
            self.focus() 
            return

        res = app.db.check_user_exists(email, password)
        if res:
            self._clear_entries()
            user = app.db.return_user_data(email, password)
            app.show_user_screen(user)
        else:
            messagebox.showinfo(title="Error", message="Incorrect user email or password")

    def return_postion_of_window(self):
        return (self.winfo_x(), self.winfo_y())
    
    def set_new_postion_of_window(self):
        self.geometry(f"{self.window_width}x{self.window_height}+{app.cords[0]}+{app.cords[1]}")


class UserScreen(ctk.CTk):
    def __init__(self, user: User):
        super().__init__()
        self.title("Library")
        self.current_user = user

        self.window_width = 350
        self.window_height = 565

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        if app.cords[0] is None:
            app.cords = ((self.screen_width // 2) - (self.window_width // 2), (self.screen_height // 2) - (self.window_height // 2))

        self.grid_columnconfigure((0, 1), weight=1)
        self.resizable(False, False)

        self._profile_screen()

    def _profile_screen(self):
        self._clear_window()
        self.current_page = "Profile"

        menu = ctk.CTkOptionMenu(self, width=35, height=35, values=["Profile", "Borrow books", "Return books", "Sign out", "Delete account"], dynamic_resizing=False, font=("Roboto", 1), command=self._change_page)
        menu.grid(row=0, column=0, padx=10, pady=8, sticky="w", columnspan=2)

        profile_text_label = ctk.CTkLabel(self, text="Profile:", font=("Roboto", 30, "bold"))
        profile_text_label.grid(row=0, column=1, padx=(10, (self.window_width // 2 - 75)), pady=8, columnspan=2)

        email_data_frame = ctk.CTkFrame(self, fg_color="#2e2e2e", border_width=3)
        email_data_frame.grid(row=1, column=0, padx=25, pady=(10, 5), sticky="we", columnspan=2)

        email_text_label = ctk.CTkLabel(email_data_frame, text="email:", font=("Roboto", 14), text_color="silver")
        email_text_label.grid(row=0, column=0, padx=5, pady=(5, 0), ipadx=3, sticky="w")

        user_password_text_label = ctk.CTkLabel(email_data_frame, text=self.current_user.email, font=("Roboto", 22))
        user_password_text_label.grid(row=1, column=0, padx=5, pady=(0, 8), ipadx=3, sticky="w")

        password_data_frame = ctk.CTkFrame(self, fg_color="#2e2e2e", border_width=3)
        password_data_frame.grid(row=2, column=0, padx=25, pady=(0, 5), sticky="we", columnspan=2)

        password_text_label = ctk.CTkLabel(password_data_frame, text="password:", font=("Roboto", 14), text_color="silver")
        password_text_label.grid(row=0, column=0, padx=5, pady=(5, 0), ipadx=3, sticky="w")

        user_password_text_label = ctk.CTkLabel(password_data_frame, text=self.current_user.password, font=("Roboto", 22))
        user_password_text_label.grid(row=1, column=0, padx=5, pady=(0, 8), ipadx=3, sticky="w")

        date_data_frame = ctk.CTkFrame(self, fg_color="#2e2e2e", border_width=3)
        date_data_frame.grid(row=3, column=0, padx=25, pady=(0, 5), sticky="we", columnspan=2)

        date_text_label = ctk.CTkLabel(date_data_frame, text="account created at:", font=("Roboto", 14), text_color="silver")
        date_text_label.grid(row=0, column=0, padx=5, pady=(5, 0), ipadx=3, sticky="w")

        user_date_text_label = ctk.CTkLabel(date_data_frame, text=self.current_user.creation_date, font=("Roboto", 22))
        user_date_text_label.grid(row=1, column=0, padx=5, pady=(0, 8), ipadx=3, sticky="w")

        users_books = app.db.find_users_books(self.current_user.id)

        users_books_frame = ctk.CTkScrollableFrame(self, height=150, label_text="User's books:", label_font=("Roboto", 20), border_width=3)
        users_books_frame.grid_columnconfigure(0, weight=1)
        users_books_frame.grid(row=4, column=0, padx=25, pady=(2, 10), columnspan=2, rowspan=1, sticky="we")

        for i, row in enumerate(users_books.itertuples(index=False)):
            book = ctk.CTkLabel(users_books_frame, text=f"{row.title} | {row.categories}", font=("Roboto", 12))
            book.grid(row=i, column=0, padx=4, pady=1, sticky="we")


    def _clear_window(self):
        for element in self.winfo_children():
            element.destroy()

    def _close_user_screen(self):
        self.current_user = None
        app.show_sign_in_screen()

    def _change_page(self, command):
        if self.current_page == command:
            return
        elif command == "Profile":
            self._profile_screen()
        elif command == "Sign out":
            self._close_user_screen()
        elif command == "Delete account":
            ask_to_delete = messagebox.askyesno(title="Delete account", message="Are you sure you want to delete your account?")
            if ask_to_delete:
                app.db.delete_user(user_email=self.current_user.email, user_password=self.current_user.password)
                self._close_user_screen()
            else:
                return

    def return_postion_of_window(self):
        return (self.winfo_x(), self.winfo_y())
    
    def set_new_postion_of_window(self):
        self.geometry(f"{self.window_width}x{self.window_height}+{app.cords[0]}+{app.cords[1]}")


class App:
    def __init__(self):
        self.db = DataBase()
        self.cords = (None, None)
        self.current_window = None
        self.sign_in_screen = None
        self.sign_up_screen = None
        self.user_screen = None

    def _check_current_window(self):
        if self.current_window is not None:
            self.cords = self.current_window.return_postion_of_window()
            self.current_window.withdraw()

    def show_user_screen(self, user: User):
        self._check_current_window()

        if self.user_screen is None:
            self.user_screen = UserScreen(user)
            self.user_screen.protocol("WM_DELETE_WINDOW", self.end)
        else:
            self.user_screen.current_user = user
            self.user_screen._profile_screen()
            self.user_screen.deiconify()
        
        self.user_screen.set_new_postion_of_window()
        self.current_window = self.user_screen
        self.user_screen.mainloop()


    def show_sign_up_screen(self):
        self._check_current_window()

        if self.sign_up_screen is None:
            self.sign_up_screen = SignUpScreen()
            self.sign_up_screen.protocol("WM_DELETE_WINDOW", self.end)
        else:
            self.sign_up_screen.deiconify()

        self.sign_up_screen.set_new_postion_of_window()
        self.current_window = self.sign_up_screen
        self.sign_up_screen.mainloop()

    def show_sign_in_screen(self):
        self._check_current_window()

        if self.sign_in_screen is None:
            self.sign_in_screen = SignInScreen()
            self.sign_in_screen.protocol("WM_DELETE_WINDOW", self.end)
        else:
            self.sign_in_screen.deiconify()

        self.sign_in_screen.set_new_postion_of_window()
        self.current_window = self.sign_in_screen
        self.sign_in_screen.mainloop()

    def start(self):
        self.show_sign_in_screen()

    def end(self):
        self.db.close_db()
        if self.sign_in_screen is not None: self.sign_in_screen.destroy()
        if self.sign_up_screen is not None: self.sign_up_screen.destroy()
        if self.user_screen is not None: self.user_screen.destroy()
        print("Aplikacja została wyłączona...") 


def main():
    global app
    app = App()
    app.start()


if __name__ == '__main__':
    main()