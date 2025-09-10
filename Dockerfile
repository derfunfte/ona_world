FROM aladdin1234/xtts-webui:0.2

# Set working directory
WORKDIR /app

# Copy requirements.txt first for better Docker layer caching
COPY requirements.txt .

# Entfernen der bestehenden virtuellen Umgebung
RUN rm -rf /venv

# Erstellen einer neuen virtuellen Umgebung
RUN python3 -m venv /venv

# Aktivieren der virtuellen Umgebung und Installieren der Abhängigkeiten
RUN /venv/bin/pip install --upgrade pip setuptools wheel

# Installieren der Abhängigkeiten aus der requirements.txt
RUN /venv/bin/pip install -r requirements.txt

# Copy application files
COPY . .

# Create output directory
RUN mkdir -p output

# Expose port for the application
EXPOSE 7860

# Set environment variables
ENV PATH="/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Default command to run the application
CMD ["/venv/bin/python", "meine_stimme_app.py"]