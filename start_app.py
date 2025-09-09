#!/usr/bin/env python3
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
    gr.Markdown("Einfache Text-zu-Sprache Anwendung mit espeak")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text eingeben",
                placeholder="Geben Sie hier Ihren Text ein...",
                lines=4
            )
            voice_dropdown = gr.Dropdown(
                choices=["de", "en", "fr", "es"],
                value="de",
                label="Sprache auswählen"
            )
            generate_btn = gr.Button("🎵 Sprache generieren", variant="primary")
        
        with gr.Column():
            audio_output = gr.Audio(label="Generierte Sprache")
            status_output = gr.Textbox(label="Status", interactive=False)
    
    generate_btn.click(
        fn=text_to_speech,
        inputs=[text_input, voice_dropdown],
        outputs=[audio_output, status_output]
    )

if __name__ == "__main__":
    print("🚀 Starte Meine Stimme Anwendung...")
    app.launch(
        server_name="0.0.0.0",
        server_port=8000,
        share=False,
        show_error=True
    )