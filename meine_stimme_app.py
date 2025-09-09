#!/usr/bin/env python3
"""
Meine Stimme - Einfache Text-zu-Sprache Anwendung
Alternative zu XTTS für diese Umgebung
"""

import gradio as gr
import subprocess
import os
from pathlib import Path

# Ausgabeordner erstellen
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

def text_to_speech(text, voice="de"):
    """
    Konvertiert Text zu Sprache mit espeak
    """
    if not text.strip():
        return None, "Bitte geben Sie Text ein."
    
    # Dateiname generieren
    filename = f"output_{len(os.listdir(output_dir)) + 1}.wav"
    filepath = output_dir / filename
    
    try:
        # espeak für Text-zu-Sprache verwenden
        cmd = [
            "espeak", 
            "-v", voice,
            "-s", "150",  # Geschwindigkeit
            "-w", str(filepath),  # Ausgabedatei
            text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return str(filepath), f"✅ Erfolgreich erstellt: {filename}"
        else:
            return None, f"❌ Fehler: {result.stderr}"
            
    except FileNotFoundError:
        return None, "❌ espeak ist nicht installiert. Installiere mit: sudo apt install espeak"
    except Exception as e:
        return None, f"❌ Fehler: {str(e)}"

def list_voices():
    """Liste verfügbare Stimmen auf"""
    try:
        result = subprocess.run(["espeak", "--voices"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return "Fehler beim Abrufen der Stimmen"
    except:
        return "espeak nicht verfügbar"

# Gradio Interface
with gr.Blocks(title="Meine Stimme - Text zu Sprache") as app:
    gr.Markdown("# 🎤 Meine Stimme - Text zu Sprache")
    gr.Markdown("Einfache Text-zu-Sprache Anwendung mit espeak")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text eingeben",
                placeholder="Geben Sie hier Ihren Text ein...",
                lines=5
            )
            
            voice_dropdown = gr.Dropdown(
                choices=["de", "en", "fr", "es", "it"],
                value="de",
                label="Sprache auswählen"
            )
            
            generate_btn = gr.Button("🎵 Sprache generieren", variant="primary")
        
        with gr.Column():
            audio_output = gr.Audio(label="Generierte Sprache")
            status_output = gr.Textbox(label="Status", interactive=False)
    
    # Event Handler
    generate_btn.click(
        fn=text_to_speech,
        inputs=[text_input, voice_dropdown],
        outputs=[audio_output, status_output]
    )
    
    # Informationen
    with gr.Accordion("ℹ️ Informationen", open=False):
        gr.Markdown("""
        **Verfügbare Sprachen:**
        - `de` - Deutsch
        - `en` - Englisch  
        - `fr` - Französisch
        - `es` - Spanisch
        - `it` - Italienisch
        
        **Ausgabeordner:** `./output/`
        
        **Hinweis:** Diese Anwendung verwendet espeak als TTS-Engine.
        """)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=8080, share=False)