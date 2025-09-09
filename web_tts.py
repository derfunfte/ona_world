#!/usr/bin/env python3
"""
Einfache Web-TTS Anwendung mit Flask
"""

from flask import Flask, render_template_string, request, send_file, jsonify
import subprocess
import os
from pathlib import Path

app = Flask(__name__)

# Ausgabeordner erstellen
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎤 Meine Stimme - Text zu Sprache</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 10px; }
        textarea { width: 100%; height: 100px; margin: 10px 0; padding: 10px; }
        select, button { padding: 10px; margin: 5px; }
        button { background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 10px; background: white; border-radius: 5px; }
        audio { width: 100%; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎤 Meine Stimme - Text zu Sprache</h1>
        <p>Einfache Text-zu-Sprache Anwendung mit espeak</p>
        
        <form id="ttsForm">
            <textarea id="text" placeholder="Geben Sie hier Ihren Text ein..." required></textarea>
            <br>
            <select id="voice">
                <option value="de">Deutsch</option>
                <option value="en">English</option>
                <option value="fr">Français</option>
                <option value="es">Español</option>
            </select>
            <button type="submit">🎵 Sprache generieren</button>
        </form>
        
        <div id="result" class="result" style="display: none;">
            <h3>Ergebnis:</h3>
            <div id="status"></div>
            <audio id="audio" controls style="display: none;"></audio>
        </div>
    </div>

    <script>
        document.getElementById('ttsForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const text = document.getElementById('text').value;
            const voice = document.getElementById('voice').value;
            const resultDiv = document.getElementById('result');
            const statusDiv = document.getElementById('status');
            const audioElement = document.getElementById('audio');
            
            statusDiv.innerHTML = '⏳ Generiere Sprache...';
            resultDiv.style.display = 'block';
            audioElement.style.display = 'none';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text, voice: voice })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    statusDiv.innerHTML = '✅ ' + result.message;
                    audioElement.src = '/audio/' + result.filename;
                    audioElement.style.display = 'block';
                } else {
                    statusDiv.innerHTML = '❌ ' + result.message;
                }
            } catch (error) {
                statusDiv.innerHTML = '❌ Fehler: ' + error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    text = data.get('text', '').strip()
    voice = data.get('voice', 'de')
    
    if not text:
        return jsonify({'success': False, 'message': 'Bitte geben Sie Text ein.'})
    
    filename = f"output_{len(os.listdir(output_dir)) + 1}.wav"
    filepath = output_dir / filename
    
    try:
        cmd = ["espeak", "-v", voice, "-s", "150", "-w", str(filepath), text]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return jsonify({
                'success': True, 
                'message': f'Erfolgreich erstellt: {filename}',
                'filename': filename
            })
        else:
            return jsonify({'success': False, 'message': f'Fehler: {result.stderr}'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Fehler: {str(e)}'})

@app.route('/audio/<filename>')
def serve_audio(filename):
    filepath = output_dir / filename
    if filepath.exists():
        return send_file(filepath, as_attachment=False)
    else:
        return "Datei nicht gefunden", 404

if __name__ == '__main__':
    print("🚀 Starte Meine Stimme Web-Anwendung...")
    print("📍 URL: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=False)