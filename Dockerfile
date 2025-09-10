FROM aladdin1234/xtts-webui:0.2

# Entfernen der bestehenden virtuellen Umgebung
RUN rm -rf /venv

# Erstellen einer neuen virtuellen Umgebung
RUN python3 -m venv /venv

# Aktivieren der virtuellen Umgebung und Installieren der Abhängigkeiten
RUN /venv/bin/pip install --upgrade pip setuptools wheel

# Installieren der Abhängigkeiten aus der requirements.txt (falls vorhanden)
COPY requirements.txt /venv/xtts/requirements.txt
RUN /venv/bin/pip install -r /venv/xtts/requirements.txt
