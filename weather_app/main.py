import os
from database.db_manager import DBManager
from utils.helpers import prepare_icons
from app import App

def main():
    # Ensure database is initialized
    DBManager.initialize()
    
    # Prepare icons if needed
    prepare_icons()
    
    app = App()
    
    # Try setting icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    if os.path.exists(icon_path) and os.name == 'nt':
        app.iconbitmap(icon_path)
    # else could use iconphoto for Linux/macOS
    
    app.mainloop()

if __name__ == "__main__":
    main()
