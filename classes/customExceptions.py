class MenuError(Exception):
    """Invalid input on menu screen"""
    pass

class BackToMenu(Exception):
    """User would like to go back to the main menu"""
    pass
