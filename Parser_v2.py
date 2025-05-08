import tkinter as tk
from tkinter import scrolledtext, END, font as tkfont
import re
import difflib

# --- Kernlogik ---
def normalize_quotes(text):
    """
    Ersetzt verschiedene Unicode-Anführungszeichen durch Standard-ASCII-Anführungszeichen.
    """
    quote_map = {
        '\u201c': '"',  # “ LEFT DOUBLE QUOTATION MARK
        '\u201d': '"',  # ” RIGHT DOUBLE QUOTATION MARK
        '\u201e': '"',  # „ DOUBLE LOW-9 QUOTATION MARK
        '\u00ab': '"',  # « LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
        '\u00bb': '"',  # » RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        '\u2018': "'",  # ‘ LEFT SINGLE QUOTATION MARK
        '\u2019': "'",  # ’ RIGHT SINGLE QUOTATION MARK
    }
    for fancy_quote, standard_quote in quote_map.items():
        text = text.replace(fancy_quote, standard_quote)
    return text

def extrahiere_funde_aus_datensatz(text_listen_str):
    """
    Analysiert den Haupt-Datensatz.
    Extrahiert Phrasen in doppelten Anführungszeichen, einfachen Anführungszeichen,
    Text in Klammern, Text zwischen Schrägstrichen und prüft auf spezielle Hinweis-Phrasen.
    Gibt eine Liste von Funden (Typ, Text), eine Statusmeldung und eine Liste von Hinweismeldungen zurück.
    Typen: 'zitat', 'klammer', 'slash_text', 'single_quote_text'
    """
    normalized_text_listen_str = normalize_quotes(text_listen_str)
    verarbeiteter_input = normalized_text_listen_str.strip()
    
    actual_item_contents = []
    is_single_item_input = False # Flag to indicate if the input was a single "target question" item

    # Behandlung für Eingaben, die mit {"target question": beginnen
    if verarbeiteter_input.startswith('{"target question":'):
        is_single_item_input = True
        prefix = '{"target question":'
        try:
            # Finde den Start des Wert-Strings (erstes Anführungszeichen nach dem Prefix-Teil)
            value_start_quote_index = verarbeiteter_input.index('"', len(prefix))
            # Der eigentliche Wert beginnt nach diesem Anführungszeichen
            value_start_index = value_start_quote_index + 1
            
            # Finde das Ende des Wert-Strings (letztes Anführungszeichen vor der schließenden '}')
            closing_brace_index = verarbeiteter_input.rfind('}')
            if closing_brace_index == -1: # Sollte nicht passieren, wenn startswith und strip korrekt waren
                return [], "Fehler: Ungültiges 'target question' Format (fehlende schließende Klammer '}')", []

            value_end_index = verarbeiteter_input.rfind('"', value_start_index, closing_brace_index)

            if value_start_index < value_end_index :
                extracted_sentence = verarbeiteter_input[value_start_index:value_end_index]
                actual_item_contents = [extracted_sentence.strip()] # Als einzelnes Element behandeln
            else:
                return [], "Fehler: Wert für 'target question' konnte nicht extrahiert werden (Anführungszeichen fehlen oder sind falsch platziert).", []
        except ValueError: # index oder rfind hat das Zeichen nicht gefunden
            return [], "Fehler: Ungültiges Format für 'target question'. Anführungszeichen oder Doppelpunkt fehlen.", []
    
    if not is_single_item_input:
        # Bestehende Logik für listenartige Eingaben
        if verarbeiteter_input.startswith('"') and verarbeiteter_input.endswith('"') and len(verarbeiteter_input) > 1:
            temp_stripped = verarbeiteter_input[1:-1].strip()
            if temp_stripped.startswith('[') and temp_stripped.endswith(']'):
                verarbeiteter_input = temp_stripped

        if not (verarbeiteter_input.startswith('[') and verarbeiteter_input.endswith(']')):
            return [], "Fehler: Originaltext nicht als Liste erkannt (muss mit '[' beginnen und mit ']' enden).", []

        list_content_str = verarbeiteter_input[1:-1].strip()

        if not list_content_str:
            return [], "Der eingegebene Originaltext (Liste) ist leer.", []

        list_of_quoted_segments = re.split(r',(?=(?:[^"]*"[^"]*")*[^"]*$)', list_content_str)
        
        for segment in list_of_quoted_segments:
            processed_segment = segment.strip()
            if processed_segment.startswith('"') and processed_segment.endswith('"'):
                content = processed_segment[1:-1] 
                actual_item_contents.append(content)
            elif processed_segment: 
                 return [], f"Fehler beim Parsen eines Segments im Originaltext: '{processed_segment}'. Stellen Sie sicher, dass alle Listenelemente in Anführungszeichen stehen.", []

    # --- Ab hier ist die Verarbeitung für actual_item_contents gleich, egal ob einzeln oder Liste ---
    alle_funde = [] 
    hinweis_meldungen_fuer_ausgabe = []
    regex_zitat = r'"([^"]*)"'
    regex_single_quote = r"'([^']*)'"
    regex_klammer = r'\(([^)]*)\)'
    regex_slash = r'/([^/]*)/'

    hinweis_phrasen_map = {
        "alphabetical order": "HINWEIS: 'alphabetical order' gefunden. Bitte finale Übersetzung prüfen.",
        "abab rhyme": "HINWEIS: 'ABAB rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "aabb rhyme": "HINWEIS: 'AABB rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "abba rhyme": "HINWEIS: 'ABBA rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "cbbc rhyme": "HINWEIS: 'CBBC rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "abcd rhyme": "HINWEIS: 'ABCD rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "cdcd rhyme": "HINWEIS: 'CDCD rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "efef rhyme": "HINWEIS: 'EFEF rhyme' gefunden. Bitte finale Übersetzung prüfen.",
        "gg rhyme": "HINWEIS: 'GG rhyme' (Couplet) gefunden. Bitte finale Übersetzung prüfen.",
        "rhyme": "HINWEIS: 'rhyme' (oder eine Variante) gefunden. Bitte finale Übersetzung auf Reimschema prüfen.",
        "syllables": "HINWEIS: 'syllables' gefunden. Bitte finale Übersetzung prüfen.",
        "syllable": "HINWEIS: 'syllable' gefunden. Bitte finale Übersetzung prüfen."
    }
    geordnete_hinweis_keys = [
        "abab rhyme", "aabb rhyme", "abba rhyme", "cbbc rhyme", 
        "abcd rhyme", "cdcd rhyme", "efef rhyme", "gg rhyme",
        "alphabetical order", "syllables", "syllable", "rhyme"
    ]

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
        for phrase_key in geordnete_hinweis_keys:
            if phrase_key in element_string_lower:
                botschaft = hinweis_phrasen_map[phrase_key]
                if botschaft not in hinweis_meldungen_fuer_ausgabe:
                    hinweis_meldungen_fuer_ausgabe.append(botschaft)
        
    if not alle_funde and not actual_item_contents and not hinweis_meldungen_fuer_ausgabe: 
         if not actual_item_contents and not (verarbeiteter_input.startswith('[') and verarbeiteter_input.endswith(']')): 
             pass 
         elif not actual_item_contents: 
             return [], "Der eingegebene Originaltext (Liste) ist leer.", []
    return alle_funde, None, hinweis_meldungen_fuer_ausgabe

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
def prozess_eingabe():
    try:
        user_input_datensatz = eingabe_feld_datensatz.get("1.0", END).strip()
        user_input_vergleichstext = eingabe_feld_vergleich.get("1.0", END).strip()
        
        ausgabe_konsole.configure(state='normal')
        ausgabe_konsole.delete('1.0', END)
        has_displayed_something = False

        if not user_input_datensatz:
            ausgabe_konsole.insert(END, "Bitte geben Sie einen Originaltext (Datensatz) ein.\n", 'fehler_tag')
            has_displayed_something = True
        else:
            funde_datensatz, fehlermeldung_datensatz, hinweis_meldungen = extrahiere_funde_aus_datensatz(user_input_datensatz)
            
            if fehlermeldung_datensatz:
                ausgabe_konsole.insert(END, f"Originaltext-Analyse: {fehlermeldung_datensatz}\n\n", 'fehler_tag') 
                has_displayed_something = True
            elif funde_datensatz or hinweis_meldungen: 
                ausgabe_konsole.insert(END, "\n--- Analyse Originaltext (Datensatz) ---\n", 'header_tag') 
                if funde_datensatz:
                    for typ, text in funde_datensatz:
                        ausgabe_konsole.insert(END, "- ")
                        if typ == 'zitat':
                            ausgabe_konsole.insert(END, f'"{text}"', 'zitat_tag')
                            ausgabe_konsole.insert(END, " (Zitat)\n")
                        elif typ == 'single_quote_text':
                            ausgabe_konsole.insert(END, f"'{text}'", 'single_quote_tag')
                            ausgabe_konsole.insert(END, " (Einfaches Zitat)\n")
                        elif typ == 'klammer':
                            ausgabe_konsole.insert(END, f'({text})', 'klammer_tag')
                            ausgabe_konsole.insert(END, " (Klammer)\n")
                        elif typ == 'slash_text':
                            ausgabe_konsole.insert(END, f'/{text}/', 'slash_tag')
                            ausgabe_konsole.insert(END, " (Schrägstrich-Text)\n")
                
                if hinweis_meldungen:
                    ausgabe_konsole.insert(END, "\n Wichtige Hinweise:\n", 'header_hinweis_tag')
                    for hinweis in hinweis_meldungen:
                        ausgabe_konsole.insert(END, f"- {hinweis}\n", 'hinweis_tag')

                ausgabe_konsole.insert(END, "---------------------------------------\n\n")
                has_displayed_something = True
            else:
                ausgabe_konsole.insert(END, "\nOriginaltext-Analyse: Keine Zitate, Klammern oder spezielle Hinweise gefunden.\n\n") 
                has_displayed_something = True
        
        if user_input_vergleichstext:
            if not user_input_datensatz:
                ausgabe_konsole.insert(END, "Für einen Textvergleich wird auch der Originaltext benötigt.\n", 'fehler_tag')
                has_displayed_something = True
            else:
                ausgabe_konsole.insert(END, "\n--- Textvergleich ---\n", 'header_tag') 
                text1_segmente, text2_segmente = erstelle_diff_darstellung(user_input_datensatz, user_input_vergleichstext)
                ausgabe_konsole.insert(END, "\nOriginaltext (Datensatz) mit Unterschieden:\n") 
                for text_teil, tag_name in text1_segmente: ausgabe_konsole.insert(END, text_teil, tag_name)
                ausgabe_konsole.insert(END, "\n\n")
                ausgabe_konsole.insert(END, "Vergleichstext mit Unterschieden:\n")
                for text_teil, tag_name in text2_segmente: ausgabe_konsole.insert(END, text_teil, tag_name)
                ausgabe_konsole.insert(END, "\n---------------------\n\n")
                has_displayed_something = True
        
        if not has_displayed_something: 
             ausgabe_konsole.insert(END, "Keine Analyse durchgeführt. Bitte Eingaben prüfen.\n")
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
root.title("Textanalyse-Tool")
root.geometry("750x700") 
root.resizable(False, False) 
dark_gray_bg = "#424242" # Dunkelgrau
light_text_fg = "white"   # Weiß für Text auf dunklem Hintergrund
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

def erstelle_eingabe_block(parent_frame, label_text, text_height):
    block_frame = tk.Frame(parent_frame, bg=dark_gray_bg) 
    block_frame.pack(fill=tk.X, pady=(5,5)) 
    
    label = tk.Label(block_frame, text=label_text, anchor="w", bg=dark_gray_bg, fg=light_text_fg) 
    label.pack(side=tk.TOP, fill=tk.X, pady=(0,2)) 
    
    text_widget = tk.Text(block_frame, height=text_height, wrap=tk.WORD, font=default_font, 
                          relief=tk.SOLID, borderwidth=1, bg="white", fg="black") 
    text_widget.pack(fill=tk.X, expand=True)
    return text_widget

# Eingabefelder erstellen mit REDUZIERTEN HÖHEN
eingabe_feld_datensatz = erstelle_eingabe_block(eingabe_haupt_container, "Originaltext (Datensatz):", 4) 
eingabe_feld_vergleich = erstelle_eingabe_block(eingabe_haupt_container, "Vergleichstext (optional):", 4) 

# Button zum Analysieren
analyse_button = tk.Button(eingabe_haupt_container, text="Analysieren", command=prozess_eingabe, 
                           font=bold_font, 
                           bg="#4CAF50", fg="white", relief=tk.RAISED, borderwidth=1, padx=15, pady=5) 
analyse_button.pack(pady=(10,5)) 

root.mainloop()
