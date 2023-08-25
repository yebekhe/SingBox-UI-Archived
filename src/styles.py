body_light = """
background: #eee;
color: #212d40;
"""

body_dark = """
background: #212d40;
color: #eee;
"""

connectButtonStyle = """
QPushButton {
    margin: 200px
}
"""

LineEditStyle = """
QLineEdit {{
    width: 90%;
    height: 22px;
    color: {};
    background: {};
    padding: 15px;
    border: none;
    border-radius: 6px;
}}
QLineEdit:focus {{
    background: {};
    border: 2px solid '#212d40';
}}
"""

lableStyle = """
QLabel {
    width: 90%;
    font-weight: bold;
}
"""

buttonStyle = """
.QPushButton {{
    width: 60%;
    height: 40px;
    color: {};
    background: {};
    font-size: 1em;
    font-weight: bold;
    outline: none;
    border: none;
    border-radius: 6px;
}}
.QPushButton:hover{{
    background: {};
}}
.QPushButton:pressed{{
    background: {};
}} 
.QPushButton:focus{{
    border: 1px solid black;
}}
QPushButton:disabled{{
    background: {};
}}
"""
