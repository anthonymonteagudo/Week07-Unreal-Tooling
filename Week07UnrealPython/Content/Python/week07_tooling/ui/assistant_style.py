"""Semantic action emphasis for the existing Week 7 palette.

See Course/InstructorArchive/Week07/20261015/Docs/UI/UX_STYLE_SHEET.md (workspace root). These tokens refine the current theme, not the
independent GOLF+ brand. Backend validation is deliberately outside this module.
"""
TOKENS = {
    'action': '#a9cfff',
    'action_text': '#142033',
    'surface': '#303e53',
    'text': '#eef2f8',
    'border': '#61748e',
    'focus': '#9ccaff',
    'disabled_surface': '#252d39',
    'disabled_text': '#8793a6',
}

ASSISTANT_STYLE = '''
QPushButton#apply, QPushButton#preview {
    background: %(surface)s; color: %(text)s; font-weight: 400;
}
QPushButton#apply[emphasis="primary"], QPushButton#preview[emphasis="primary"] {
    background: %(action)s; color: %(action_text)s; font-weight: 600;
}
QPushButton#apply:disabled, QPushButton#preview:disabled {
    background: %(disabled_surface)s; color: %(disabled_text)s;
    border-color: #3b485c;
}
QTableWidget:focus, QPlainTextEdit:focus { border: 2px solid %(focus)s; }
''' % TOKENS
