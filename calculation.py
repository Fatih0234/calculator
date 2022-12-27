import tkinter as tk

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)


OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"

LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class Calculator:

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("375x667")
        self.root.resizable(0,0)
        self.root.title("Calculator")

        # All along the program there will be two expression; total and current

        self.total_expression = ""
        self.current_expression = ""

        # There will be two frames
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        self.total_label, self.label = self.create_labels()

        self.digits = {
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            ".":(4,1), 0:(4,2)
        }

        self.operators = {
            "/":"\u00F7", "*":"\u00D7", "-":"-", "+":"+" 
        }

        self.buttons_frame.rowconfigure(0, weight=1)
        for i in range(1,5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()
    
    # Bind the keyboard to our application 
    def bind_keys(self):
        self.root.bind("<Return>", lambda event:self.evaluation())

        for key in self.digits:
            self.root.bind(str(key), lambda event,digit=str(key): self.add_to_expression(digit))
        
        for key in self.operators:
            self.root.bind(key, lambda event, operator=key: self.append_operators(operator))

    # Command functions

    def add_to_expression(self,value):
        self.current_expression += str(value)
        self.update_label()

    def append_operators(self, operator):
        self.total_expression += self.current_expression + operator
        self.current_expression = ""
        self.update_label()
        self.update_total_label()

    def clear(self):
        self.total_expression = ""
        self.current_expression = ""
        self.update_label()
        self.update_total_label()

    def square(self):
        self.total_expression = f"sqr({self.current_expression})="
        self.current_expression = str(eval(self.current_expression+"**2"))
        self.update_label()
        self.update_total_label()

    def sqrt(self):
        self.total_expression = f"sqrt({self.current_expression})="
        self.current_expression = str(eval(self.current_expression+"**0.5"))
        self.update_total_label()
        self.update_label()

    def evaluation(self):
        self.total_expression += self.current_expression
        try:
            result = str(eval(self.total_expression))
            self.current_expression = result
            self.total_expression += "="
            self.update_total_label()
        except:
            self.current_expression = "ERROR"
            self.update_total_label()
            self.total_expression = ""
        self.total_expression = "" 
        self.update_label()     
    # Updating label and total_label

    def update_label(self):
        self.label.config(text=self.current_expression[:11])
    def update_total_label(self):
        # Let's pretify our total expression panel.
        expression = self.total_expression
        for key, val in self.operators.items():
            expression = expression.replace(key, val)
        self.total_label.config(text=expression[:11])

    # Creating display and buttons frames
    def create_display_frame(self):
        frame = tk.Frame(self.root, bg=LIGHT_GRAY, height=221)
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")
        return frame        

    # Creating buttons
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_sqrt_button()
        self.create_square_button()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2",
                            bg=WHITE, fg=LABEL_COLOR, border=0, font=DIGITS_FONT_STYLE,
                            command=self.square)
        button.grid(row=0, column=2, sticky="NSEW")

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax",
                            bg=WHITE, fg=LABEL_COLOR, border=0, font=DIGITS_FONT_STYLE,
                            command=self.sqrt)
        button.grid(row=0, column=3, sticky="NSEW")

    def create_digit_buttons(self):
        for value, cord in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(value),
                            bg=WHITE, fg=LABEL_COLOR, border=0, font=DIGITS_FONT_STYLE,
                            command=lambda x = str(value):self.add_to_expression(x)
            )
            button.grid(row=cord[0], column=cord[1], sticky="NSEW")
    
    def create_operator_buttons(self):
        i = 0
        for key, val in self.operators.items():
            button = tk.Button(self.buttons_frame, text = str(val),
            bg=OFF_WHITE, fg=LABEL_COLOR, border=0, font=DIGITS_FONT_STYLE,
            command=lambda x=str(key): self.append_operators(x)
            )
            button.grid(row=i, column=4, sticky="NSEW")
            i+=1

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C",
                        bg=WHITE, fg=LABEL_COLOR, border=0, font=DIGITS_FONT_STYLE,
                        command=self.clear
                        )
        button.grid(row=0, column=1, sticky="NSEW")

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", 
                        bg=LIGHT_BLUE, fg=LABEL_COLOR, border=0, font=DIGITS_FONT_STYLE,
                        command=self.evaluation
                        )
        button.grid(row=4, column=3,columnspan=2, sticky="NSEW")


    # Creating leabels
    def create_labels(self):
        
        total_label = tk.Label(self.display_frame, fg=LABEL_COLOR, text=self.total_expression, font=SMALL_FONT_STYLE, bg=LIGHT_GRAY)
        total_label.pack(anchor=tk.E, padx=10, pady=24)

        label = tk.Label(self.display_frame, fg=LABEL_COLOR, text=self.current_expression, font=LARGE_FONT_STYLE, bg=LIGHT_GRAY)
        label.pack(anchor=tk.E, padx=10, pady=24)
        return total_label, label



    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()



