#!/usr/bin/env python3
"""
Einfache Text-zu-Sprache Anwendung
"""

import gradio as gr
import subprocess
import os
from pathlib import Path

# Ausgabeordner erstellen
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

def text_to_speech(text, voice="de"):
    """Konvertiert Text zu Sprache mit espeak"""
    if not text.strip():
        return None, "Bitte geben Sie Text ein."
    
    filename = f"output_{len(os.listdir(output_dir)) + 1}.wav"
    filepath = output_dir / filename
    
    try:
        cmd = ["espeak", "-v", voice, "-s", "150", "-w", str(filepath), text]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return str(filepath), f"✅ Erfolgreich: {filename}"
        else:
            return None, f"❌ Fehler: {result.stderr}"
    except Exception as e:
        return None, f"❌ Fehler: {str(e)}"

# Gradio Interface
with gr.Blocks(title="Meine Stimme") as app:
    gr.Markdown("# 🎤 Meine Stimme - Text zu Sprache")
    
    with gr.Row():
        text_input = gr.Textbox(label="Text eingeben", lines=3)
        voice_dropdown = gr.Dropdown(choices=["de", "en", "fr"], value="de", label="Sprache")
    
    generate_btn = gr.Button("🎵 Generieren", variant="primary")
    
    with gr.Row():
        audio_output = gr.Audio(label="Audio")
        status_output = gr.Textbox(label="Status", interactive=False)
    
    generate_btn.click(
        fn=text_to_speech,
        inputs=[text_input, voice_dropdown],
        outputs=[audio_output, status_output]
    )

if __name__ == "__main__":
    print("🚀 Starte Meine Stimme Anwendung...")
    print("📍 URL: http://localhost:3000")
    app.launch(
        server_name="0.0.0.0", 
        server_port=3000, 
        share=False,
        show_error=True,
        quiet=False
    )