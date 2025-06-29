# 🏥 Doctor-Patient Appointment Management System

This is a modular Python project that helps manage doctor–patient appointments. It features:

- A Flask-based microservice API
- A Tkinter-based GUI with multiple tabs (Doctors, Patients, Admin)
- SQLite database (auto-generated and file-based)
- Modular clean architecture inspired by Uncle Bob's Clean Code principles
- Ready to deploy locally or on AWS

---

## 📁 Project Structure

```
doctor-appointments/
├── src/
│   ├── data/                  # SQLite schema and database access layer
│   ├── service/               # Business logic for entity operations
│   ├── interface/
│   │   ├── api/               # Flask API code
│   │   └── ui/
│   │       ├── main_ui.py     # Tkinter UI launcher
│   │       └── tabs/          # Modular tab UIs: doctor, patient, admin
├── scripts/
│   ├── migrate.py             # Create DB schema
│   └── bootstrap.py           # Insert sample doctors and patients
├── requirements.txt
├── hospital.db                # Auto-generated SQLite DB (after setup)
└── README.md
```

---

## ✅ Step-by-Step Setup (Local Machine)

### Step 1: Clone this repository

```bash
git clone https://github.com/<your-org-or-username>/doctor-appointments.git
cd doctor-appointments
```

### Step 2: Create and activate a Python virtual environment

For Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install project dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Migrate the database and bootstrap sample data

```bash
python -m scripts.migrate
python -m scripts.bootstrap
```

### Step 5: Start the Flask API

```bash
python -m src.interface.api.app
```

### Step 6: Run the Tkinter UI

```bash
python -m src.interface.ui.main_ui
```

---

## ☁️ Hosting the API on AWS EC2 (Optional)

### Step 1: Launch an EC2 instance

Use Amazon Linux, allow inbound ports 22 and 80.

### Step 2: Connect to your EC2 instance

```bash
ssh -i your-key.pem ec2-user@<your-ec2-public-ip>
```

### Step 3: Install system packages

```bash
sudo yum update -y
sudo yum install git python3 python3-venv nginx -y
```

### Step 4: Clone the repo and setup environment

```bash
git clone https://github.com/<your-org-or-username>/doctor-appointments.git
cd doctor-appointments
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5: Migrate and seed the database

```bash
python -m scripts.migrate
python -m scripts.bootstrap
```

### Step 6: Run Gunicorn to serve the Flask API

```bash
pip install gunicorn
gunicorn -w 3 -b 0.0.0.0:8000 src.interface.api.app:app
```

### Step 7: Configure Nginx as a reverse proxy

Create file: `/etc/nginx/conf.d/doctor.conf`

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

Reload Nginx:

```bash
sudo nginx -s reload
```

### Step 8: Set up systemd service to auto-run Gunicorn

Create `/etc/systemd/system/doctor.service`:

```ini
[Unit]
Description=Doctor API Flask App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/doctor-appointments
Environment="PATH=/home/ec2-user/doctor-appointments/venv/bin"
ExecStart=/home/ec2-user/doctor-appointments/venv/bin/gunicorn -w 3 -b 127.0.0.1:8000 src.interface.api.app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable doctor
sudo systemctl start doctor
```

---

## ✅ You’re ready to use your doctor-patient system!

- API is live on your EC2 public IP
- UI connects to local or remote API
