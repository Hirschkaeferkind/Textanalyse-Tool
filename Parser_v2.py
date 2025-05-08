import tkinter as tk
from tkinter import scrolledtext, END, font as tkfont
import re
import difflib

# --- Übersetzungen ---
translations = {
    'de': {
        'window_title': "Textanalyse-Tool",
        'label_datensatz': "Originaltext (Datensatz):",
        'label_vergleich': "Vergleichstext (optional):",
        'button_analyse': "Analysieren",
        'button_sprache': "Sprache wechseln (EN)",
        'analyse_header': "--- Analyse Originaltext (Datensatz) ---",
        'vergleich_header': "--- Textvergleich ---",
        'hinweis_header': " Wichtige Hinweise:",
        'zitat_label': "(Zitat)",
        'klammer_label': "(Klammer)",
        'single_quote_label': "(Einfaches Zitat)",
        'slash_label': "(Schrägstrich-Text)",
        'error_no_datensatz': "Bitte geben Sie einen Originaltext (Datensatz) ein.",
        'error_no_vergleich_datensatz': "Für einen Textvergleich wird auch der Originaltext benötigt.",
        'error_liste_leer': "Der eingegebene Originaltext (Liste) ist leer.",
        'error_liste_format': "Fehler: Originaltext nicht als Liste erkannt (muss mit '[' beginnen und mit ']' enden).",
        'error_segment_parse': "Fehler beim Parsen eines Segments im Originaltext: '{segment}'. Stellen Sie sicher, dass alle Listenelemente in Anführungszeichen stehen.",
        'error_target_question_format': "Fehler: Ungültiges Format für 'target question'. Anführungszeichen oder Doppelpunkt fehlen.",
        'error_target_question_klammer': "Fehler: Ungültiges 'target question' Format (fehlende schließende Klammer '}')",
        'error_target_question_wert': "Fehler: Wert für 'target question' konnte nicht extrahiert werden (Anführungszeichen fehlen oder sind falsch platziert).",
        'error_liste_elemente_extraktion': "Konnte keine gültigen Listenelemente aus dem Originaltext extrahieren.",
        'info_keine_funde': "Originaltext-Analyse: Keine Zitate, Klammern oder spezielle Hinweise gefunden.",
        'info_keine_analyse': "Keine Analyse durchgeführt. Bitte Eingaben prüfen.",
        'diff_original_header': "Originaltext (Datensatz) mit Unterschieden:",
        'diff_vergleich_header': "Vergleichstext mit Unterschieden:",
        'hinweis_alphabetical': "HINWEIS: 'alphabetical order' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_abab': "HINWEIS: 'ABAB rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_aabb': "HINWEIS: 'AABB rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_abba': "HINWEIS: 'ABBA rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_cbbc': "HINWEIS: 'CBBC rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_abcd': "HINWEIS: 'ABCD rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_cdcd': "HINWEIS: 'CDCD rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_efef': "HINWEIS: 'EFEF rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_gg': "HINWEIS: 'GG rhyme' (Couplet) gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_rhyme': "HINWEIS: 'rhyme' (oder eine Variante) gefunden. Bitte finale Übersetzung auf Reimschema prüfen.",
        'hinweis_syllables': "HINWEIS: 'syllables' gefunden. Bitte finale Übersetzung prüfen.",
        'hinweis_syllable': "HINWEIS: 'syllable' gefunden. Bitte finale Übersetzung prüfen.",
    },
    'en': {
        'window_title': "Text Analysis Tool",
        'label_datensatz': "Original Text (Dataset):",
        'label_vergleich': "Comparison Text (optional):",
        'button_analyse': "Analyze",
        'button_sprache': "Change Language (DE)",
        'analyse_header': "--- Analysis Original Text (Dataset) ---",
        'vergleich_header': "--- Text Comparison ---",
        'hinweis_header': " Important Notes:",
        'zitat_label': "(Quote)",
        'klammer_label': "(Parentheses)",
        'single_quote_label': "(Single Quote)",
        'slash_label': "(Slash Text)",
        'error_no_datensatz': "Please enter an original text (dataset).",
        'error_no_vergleich_datensatz': "Original text is required for text comparison.",
        'error_liste_leer': "The entered original text (list) is empty.",
        'error_liste_format': "Error: Original text not recognized as a list (must start with '[' and end with ']').",
        'error_segment_parse': "Error parsing a segment in the original text: '{segment}'. Ensure all list items are enclosed in quotes.",
        'error_target_question_format': "Error: Invalid format for 'target question'. Missing quotes or colon.",
        'error_target_question_klammer': "Error: Invalid 'target question' format (missing closing brace '}')",
        'error_target_question_wert': "Error: Could not extract value for 'target question' (quotes missing or misplaced).",
        'error_liste_elemente_extraktion': "Could not extract valid list items from the original text.",
        'info_keine_funde': "Original Text Analysis: No quotes, parentheses, or special notes found.",
        'info_keine_analyse': "No analysis performed. Please check inputs.",
        'diff_original_header': "Original Text (Dataset) with Differences:",
        'diff_vergleich_header': "Comparison Text with Differences:",
        'hinweis_alphabetical': "NOTE: 'alphabetical order' found. Please check final translation.",
        'hinweis_abab': "NOTE: 'ABAB rhyme' found. Please check final translation.",
        'hinweis_aabb': "NOTE: 'AABB rhyme' found. Please check final translation.",
        'hinweis_abba': "NOTE: 'ABBA rhyme' found. Please check final translation.",
        'hinweis_cbbc': "NOTE: 'CBBC rhyme' found. Please check final translation.",
        'hinweis_abcd': "NOTE: 'ABCD rhyme' found. Please check final translation.",
        'hinweis_cdcd': "NOTE: 'CDCD rhyme' found. Please check final translation.",
        'hinweis_efef': "NOTE: 'EFEF rhyme' found. Please check final translation.",
        'hinweis_gg': "NOTE: 'GG rhyme' (couplet) found. Please check final translation.",
        'hinweis_rhyme': "NOTE: 'rhyme' (or variant) found. Please check final translation for rhyme scheme.",
        'hinweis_syllables': "NOTE: 'syllables' found. Please check final translation.",
        'hinweis_syllable': "NOTE: 'syllable' found. Please check final translation.",
    }
}

# Funktion zum Abrufen von Übersetzungen (wird später definiert, benötigt aber current_language)
def get_translation(key, **kwargs):
    """Ruft die Übersetzung für den gegebenen Schlüssel ab und formatiert sie ggf."""
    # Diese Funktion benötigt 'current_language', die nach 'root' definiert wird.
    # Stellen Sie sicher, dass diese Funktion aufgerufen wird, nachdem 'current_language' initialisiert wurde.
    lang = current_language.get()
    text = translations.get(lang, {}).get(key, f"<{key}_missing>") # Fallback, falls Schlüssel fehlt
    try:
        return text.format(**kwargs) # Ermöglicht das Einfügen von Werten, z.B. bei Fehlermeldungen
    except KeyError:
        return text # Falls Formatierung fehlschlägt oder nicht benötigt wird

# --- Kernlogik ---
def normalize_quotes(text):
    """
    Ersetzt verschiedene Unicode-Anführungszeichen durch Standard-ASCII-Anführungszeichen.
    """
    quote_map = {
        '\u201c': '"', '\u201d': '"', '\u201e': '"', '\u00ab': '"', '\u00bb': '"',
        '\u2018': "'", '\u2019': "'",
    }
    for fancy_quote, standard_quote in quote_map.items():
        text = text.replace(fancy_quote, standard_quote)
    return text

def extrahiere_funde_aus_datensatz(text_listen_str):
    """
    Analysiert den Haupt-Datensatz.
    Gibt eine Liste von Funden (Typ, Text), einen Fehler-Schlüssel oder None,
    und eine Liste von Hinweis-Schlüsseln zurück.
    """
    normalized_text_listen_str = normalize_quotes(text_listen_str)
    verarbeiteter_input = normalized_text_listen_str.strip()
    
    actual_item_contents = []
    is_single_item_input = False 

    if verarbeiteter_input.startswith('{"target question":'):
        is_single_item_input = True
        prefix = '{"target question":'
        try:
            value_start_quote_index = verarbeiteter_input.index('"', len(prefix))
            value_start_index = value_start_quote_index + 1
            closing_brace_index = verarbeiteter_input.rfind('}')
            if closing_brace_index == -1: 
                return [], 'error_target_question_klammer', []
            value_end_index = verarbeiteter_input.rfind('"', value_start_index, closing_brace_index)
            if value_start_index < value_end_index :
                extracted_sentence = verarbeiteter_input[value_start_index:value_end_index]
                actual_item_contents = [extracted_sentence.strip()] 
            else:
                return [], 'error_target_question_wert', []
        except ValueError: 
            return [], 'error_target_question_format', []
    
    if not is_single_item_input:
        if verarbeiteter_input.startswith('"') and verarbeiteter_input.endswith('"') and len(verarbeiteter_input) > 1:
            temp_stripped = verarbeiteter_input[1:-1].strip()
            if temp_stripped.startswith('[') and temp_stripped.endswith(']'):
                verarbeiteter_input = temp_stripped

        if not (verarbeiteter_input.startswith('[') and verarbeiteter_input.endswith(']')):
            return [], 'error_liste_format', []

        list_content_str = verarbeiteter_input[1:-1].strip()

        if not list_content_str:
            return [], 'error_liste_leer', []

        list_of_quoted_segments = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', list_content_str)
        
        for segment in list_of_quoted_segments:
            processed_segment = segment.strip()
            if processed_segment.startswith('"') and processed_segment.endswith('"'):
                content = processed_segment[1:-1] 
                actual_item_contents.append(content)
            elif processed_segment: 
                 # Rückgabe des Fehler-Schlüssels und des problematischen Segments für die Formatierung
                 return [], ('error_segment_parse', {'segment': processed_segment}), []

    alle_funde = [] 
    hinweis_schluessel_fuer_ausgabe = [] # Speichert jetzt nur die Schlüssel
    regex_zitat = r'"([^"]*)"'
    regex_single_quote = r"'([^']*)'"
    regex_klammer = r'\(([^)]*)\)'
    regex_slash = r'/([^/]*)/'

    # Mapping von Suchphrasen zu Hinweis-Schlüsseln
    hinweis_schluessel_map = {
        "alphabetical order": "hinweis_alphabetical",
        "abab rhyme": "hinweis_abab",
        "aabb rhyme": "hinweis_aabb",
        "abba rhyme": "hinweis_abba",
        "cbbc rhyme": "hinweis_cbbc",
        "abcd rhyme": "hinweis_abcd",
        "cdcd rhyme": "hinweis_cdcd",
        "efef rhyme": "hinweis_efef",
        "gg rhyme": "hinweis_gg",
        "rhyme": "hinweis_rhyme",
        "syllables": "hinweis_syllables",
        "syllable": "hinweis_syllable"
    }
    geordnete_hinweis_keys_intern = list(hinweis_schluessel_map.keys())
    # Sortieren, um spezifischere Reime zuerst zu prüfen
    geordnete_hinweis_keys_intern.sort(key=lambda x: (not x.endswith("rhyme"), len(x)), reverse=True)


    for element_string in actual_item_contents:
        if not isinstance(element_string, str): 
            continue
        
        zitierte_phrasen = re.findall(regex_zitat, element_string)
        for zp in zitierte_phrasen: alle_funde.append(('zitat', zp))
        
        single_quote_texte = re.findall(regex_single_quote, element_string)
        for sqt in single_quote_texte: alle_funde.append(('single_quote_text', sqt))

        klammer_texte = re.findall(regex_klammer, element_string)
        for kt in klammer_texte: alle_funde.append(('klammer', kt))

        slash_texte = re.findall(regex_slash, element_string)
        for st in slash_texte: alle_funde.append(('slash_text', st))

        element_string_lower = element_string.lower()
        for phrase_key in geordnete_hinweis_keys_intern:
            if phrase_key in element_string_lower:
                hinweis_key = hinweis_schluessel_map[phrase_key]
                if hinweis_key not in hinweis_schluessel_fuer_ausgabe:
                    hinweis_schluessel_fuer_ausgabe.append(hinweis_key)
        
    if not alle_funde and not actual_item_contents and not hinweis_schluessel_fuer_ausgabe: 
         if not actual_item_contents and not (verarbeiteter_input.startswith('[') and verarbeiteter_input.endswith(']')): 
             pass 
         elif not actual_item_contents: 
             return [], 'error_liste_leer', [] # War eine leere Liste "[]"
             
    return alle_funde, None, hinweis_schluessel_fuer_ausgabe

def erstelle_diff_darstellung(text1_str, text2_str):
    text1_str = normalize_quotes(text1_str) 
    text2_str = normalize_quotes(text2_str)
    d = difflib.SequenceMatcher(None, text1_str, text2_str)
    text1_segmente = []
    text2_segmente = []
    for tag, i1, i2, j1, j2 in d.get_opcodes():
        if tag == 'equal':
            text1_segmente.append((text1_str[i1:i2], 'diff_common_tag'))
            text2_segmente.append((text2_str[j1:j2], 'diff_common_tag'))
        elif tag == 'delete': 
            text1_segmente.append((text1_str[i1:i2], 'diff_deleted_tag'))
        elif tag == 'insert': 
            text2_segmente.append((text2_str[j1:j2], 'diff_added_tag'))
        elif tag == 'replace':
            text1_segmente.append((text1_str[i1:i2], 'diff_deleted_tag')) 
            text2_segmente.append((text2_str[j1:j2], 'diff_added_tag'))   
    return text1_segmente, text2_segmente

# --- GUI-spezifischer Code ---
def update_ui_texts():
    """Aktualisiert alle statischen Texte der GUI basierend auf der aktuellen Sprache."""
    lang = current_language.get()
    root.title(get_translation('window_title'))
    label_datensatz.config(text=get_translation('label_datensatz'))
    label_vergleich.config(text=get_translation('label_vergleich'))
    analyse_button.config(text=get_translation('button_analyse'))
    sprache_wechseln_button.config(text=get_translation('button_sprache'))

def toggle_language():
    """Wechselt die Sprache und aktualisiert die GUI."""
    if current_language.get() == 'de':
        current_language.set('en')
    else:
        current_language.set('de')
    update_ui_texts()
    ausgabe_konsole.configure(state='normal')
    ausgabe_konsole.insert('1.0', f"Sprache auf '{current_language.get().upper()}' geändert.\nLanguage changed to '{current_language.get().upper()}'.\n\n", 'hinweis_tag')
    ausgabe_konsole.configure(state='disabled')

def prozess_eingabe():
    try:
        user_input_datensatz = eingabe_feld_datensatz.get("1.0", END).strip()
        user_input_vergleichstext = eingabe_feld_vergleich.get("1.0", END).strip()
        
        ausgabe_konsole.configure(state='normal')
        ausgabe_konsole.delete('1.0', END)
        has_displayed_something = False

        if not user_input_datensatz:
            ausgabe_konsole.insert(END, get_translation('error_no_datensatz') + "\n", 'fehler_tag')
            has_displayed_something = True
        else:
            funde_datensatz, fehlermeldung_key, hinweis_schluessel = extrahiere_funde_aus_datensatz(user_input_datensatz)
            
            fehler_text = None
            if isinstance(fehlermeldung_key, tuple): 
                 fehler_text = get_translation(fehlermeldung_key[0], **fehlermeldung_key[1])
            elif isinstance(fehlermeldung_key, str): 
                 fehler_text = get_translation(fehlermeldung_key)

            if fehler_text:
                ausgabe_konsole.insert(END, f"{get_translation('analyse_header')}: {fehler_text}\n\n", 'fehler_tag') 
                has_displayed_something = True
            elif funde_datensatz or hinweis_schluessel: 
                ausgabe_konsole.insert(END, f"\n{get_translation('analyse_header')}\n", 'header_tag') 
                if funde_datensatz:
                    for typ, text in funde_datensatz:
                        ausgabe_konsole.insert(END, "- ")
                        if typ == 'zitat':
                            ausgabe_konsole.insert(END, f'"{text}"', 'zitat_tag')
                            ausgabe_konsole.insert(END, f" {get_translation('zitat_label')}\n")
                        elif typ == 'single_quote_text':
                            ausgabe_konsole.insert(END, f"'{text}'", 'single_quote_tag')
                            ausgabe_konsole.insert(END, f" {get_translation('single_quote_label')}\n")
                        elif typ == 'klammer':
                            ausgabe_konsole.insert(END, f'({text})', 'klammer_tag')
                            ausgabe_konsole.insert(END, f" {get_translation('klammer_label')}\n")
                        elif typ == 'slash_text':
                            ausgabe_konsole.insert(END, f'/{text}/', 'slash_tag')
                            ausgabe_konsole.insert(END, f" {get_translation('slash_label')}\n")
                
                if hinweis_schluessel:
                    ausgabe_konsole.insert(END, f"\n{get_translation('hinweis_header')}\n", 'header_hinweis_tag')
                    for hinweis_key in hinweis_schluessel:
                        ausgabe_konsole.insert(END, f"- {get_translation(hinweis_key)}\n", 'hinweis_tag')

                ausgabe_konsole.insert(END, "---------------------------------------\n\n")
                has_displayed_something = True
            else:
                ausgabe_konsole.insert(END, f"\n{get_translation('info_keine_funde')}\n\n") 
                has_displayed_something = True
        
        if user_input_vergleichstext:
            if not user_input_datensatz:
                ausgabe_konsole.insert(END, get_translation('error_no_vergleich_datensatz') + "\n", 'fehler_tag')
                has_displayed_something = True
            else:
                ausgabe_konsole.insert(END, f"\n{get_translation('vergleich_header')}\n", 'header_tag') 
                text1_segmente, text2_segmente = erstelle_diff_darstellung(user_input_datensatz, user_input_vergleichstext)
                ausgabe_konsole.insert(END, f"\n{get_translation('diff_original_header')}\n") 
                for text_teil, tag_name in text1_segmente: ausgabe_konsole.insert(END, text_teil, tag_name)
                ausgabe_konsole.insert(END, "\n\n")
                ausgabe_konsole.insert(END, f"{get_translation('diff_vergleich_header')}\n")
                for text_teil, tag_name in text2_segmente: ausgabe_konsole.insert(END, text_teil, tag_name)
                ausgabe_konsole.insert(END, "\n---------------------\n\n")
                has_displayed_something = True
        
        if not has_displayed_something: 
             ausgabe_konsole.insert(END, get_translation('info_keine_analyse') + "\n")
        eingabe_feld_datensatz.delete("1.0", END)
        eingabe_feld_vergleich.delete("1.0", END)
        
    except Exception as e_outer_gui:
        print(f"TERMINAL DEBUG: Exception in prozess_eingabe (GUI handling): {e_outer_gui}")
        try:
            if ausgabe_konsole.cget("state") == 'disabled': ausgabe_konsole.configure(state='normal')
            ausgabe_konsole.insert(END, f"Schwerwiegender Fehler in der GUI-Verarbeitung: {e_outer_gui}\n", 'fehler_tag')
        except Exception as e_report_gui: print(f"TERMINAL DEBUG: Konnte Fehler nicht in GUI-Konsole berichten: {e_report_gui}")
    finally:
        try:
            if ausgabe_konsole: ausgabe_konsole.configure(state='disabled')
        except Exception as e_final_config: print(f"TERMINAL DEBUG: Fehler beim finalen Deaktivieren der Konsole: {e_final_config}")

# Hauptfenster erstellen
root = tk.Tk()
# *** KORREKTUR: Globale Variable NACH root = tk.Tk() definieren ***
current_language = tk.StringVar(value='de') # Standardmäßig Deutsch

root.geometry("750x700") 
root.resizable(False, False) 
dark_gray_bg = "#424242" 
light_text_fg = "white"   
root.configure(bg=dark_gray_bg)

default_font_family = "Arial"
default_font_size = 10
default_font = tkfont.Font(family=default_font_family, size=default_font_size)
root.option_add("*Font", default_font) 

bold_font = tkfont.Font(family=default_font_family, size=default_font_size, weight="bold")
italic_font = tkfont.Font(family=default_font_family, size=default_font_size, slant="italic")
strikethrough_font = tkfont.Font(family=default_font_family, size=default_font_size, overstrike=True)
header_font = tkfont.Font(family=default_font_family, size=default_font_size + 2, weight="bold") 
hinweis_font = tkfont.Font(family=default_font_family, size=default_font_size, weight="bold")

# Stil für die Ausgabe-Konsole
ausgabe_konsole = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, state='disabled', font=default_font, bg="white", fg="black") 
ausgabe_konsole.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Tags für farbige Ausgabe konfigurieren
ausgabe_konsole.tag_configure('zitat_tag', foreground='red', font=bold_font)
ausgabe_konsole.tag_configure('single_quote_tag', foreground='orange', font=italic_font) 
ausgabe_konsole.tag_configure('klammer_tag', foreground='green', font=italic_font)
ausgabe_konsole.tag_configure('slash_tag', foreground='purple', font=italic_font) 
ausgabe_konsole.tag_configure('fehler_tag', foreground='orange red', font=italic_font)
ausgabe_konsole.tag_configure('header_tag', font=header_font) 
ausgabe_konsole.tag_configure('hinweis_tag', foreground='magenta', font=hinweis_font) 
ausgabe_konsole.tag_configure('header_hinweis_tag', font=header_font, foreground='magenta') 

ausgabe_konsole.tag_configure('diff_common_tag', foreground='black', font=default_font) 
ausgabe_konsole.tag_configure('diff_deleted_tag', foreground='#D32F2F', font=strikethrough_font) 
ausgabe_konsole.tag_configure('diff_added_tag', foreground='#388E3C', font=bold_font) 

# Hauptrahmen für alle Eingabebereiche
eingabe_haupt_container = tk.Frame(root, bg=dark_gray_bg) 
eingabe_haupt_container.pack(padx=10, pady=(0,10), fill=tk.X)

# Funktion zum Erstellen eines Eingabe-Blocks (Label + Textfeld)
def erstelle_eingabe_block(parent_frame, label_text_key, text_height):
    block_frame = tk.Frame(parent_frame, bg=dark_gray_bg) 
    block_frame.pack(fill=tk.X, pady=(5,5)) 
    
    # Label wird jetzt global gespeichert, um Text aktualisieren zu können
    label = tk.Label(block_frame, text=get_translation(label_text_key), anchor="w", bg=dark_gray_bg, fg=light_text_fg) 
    label.pack(side=tk.TOP, fill=tk.X, pady=(0,2)) 
    
    text_widget = tk.Text(block_frame, height=text_height, wrap=tk.WORD, font=default_font, 
                          relief=tk.SOLID, borderwidth=1, bg="white", fg="black") 
    text_widget.pack(fill=tk.X, expand=True)
    # Gib Label und Textfeld zurück
    return label, text_widget

# Eingabefelder erstellen und Labels speichern
label_datensatz, eingabe_feld_datensatz = erstelle_eingabe_block(eingabe_haupt_container, 'label_datensatz', 4) 
label_vergleich, eingabe_feld_vergleich = erstelle_eingabe_block(eingabe_haupt_container, 'label_vergleich', 4) 

# Rahmen für die Buttons am unteren Rand
button_rahmen = tk.Frame(eingabe_haupt_container, bg=dark_gray_bg)
button_rahmen.pack(pady=(10,5))

# Button zum Analysieren
analyse_button = tk.Button(button_rahmen, text=get_translation('button_analyse'), command=prozess_eingabe, 
                           font=bold_font, 
                           bg="#4CAF50", fg="white", relief=tk.RAISED, borderwidth=1, padx=15, pady=5) 
analyse_button.pack(side=tk.LEFT, padx=(0, 10)) # Links im Button-Rahmen

# Button zum Sprache wechseln
sprache_wechseln_button = tk.Button(button_rahmen, text=get_translation('button_sprache'), command=toggle_language,
                                    font=default_font, relief=tk.RAISED, borderwidth=1, padx=10, pady=5)
sprache_wechseln_button.pack(side=tk.LEFT) # Rechts neben dem Analyse-Button


# Initialisiere die UI-Texte beim Start
update_ui_texts()

# Start der GUI-Schleife
root.mainloop()
