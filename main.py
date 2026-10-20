from database import create_tables
from gui import LoginWindow

create_tables()

app = LoginWindow()
app.mainloop()
