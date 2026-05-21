from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import qrcode
from datetime import datetime
import json
import os
import hashlib
from urllib.parse import urlparse
from io import BytesIO
import base64
from collections import defaultdict
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)
app.secret_key = 'cybersecurity-awareness-training-key-2026'

# Ensure directories exist
os.makedirs('analytics', exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Data storage (in production, use a database)
class AwarenessLab:
    def __init__(self):
        self.visits = []
        self.attempts = []
        self.qr_scans = []
        self.load_data()
    
    def load_data(self):
        """Load existing data from files"""
        try:
            with open('analytics/visits.json', 'r') as f:
                self.visits = json.load(f)
        except:
            pass
        try:
            with open('analytics/attempts.json', 'r') as f:
                self.attempts = json.load(f)
        except:
            pass
    
    def save_data(self):
        """Save data to files"""
        with open('analytics/visits.json', 'w') as f:
            json.dump(self.visits[-1000:], f)  # Keep last 1000 records
        with open('analytics/attempts.json', 'w') as f:
            json.dump(self.attempts[-1000:], f)
    
    def add_visit(self, ip, user_agent, qr_source=False):
        visit = {
            'ip': ip,
            'user_agent': user_agent,
            'timestamp': datetime.now().isoformat(),
            'qr_source': qr_source
        }
        self.visits.append(visit)
        self.save_data()
        return visit
    
    def add_attempt(self, email, ip, user_agent):
        # Hash email for privacy (but keep for training)
        email_hash = hashlib.sha256(email.encode()).hexdigest()[:16]
        attempt = {
            'email_hash': email_hash,
            'email_domain': email.split('@')[-1] if '@' in email else 'unknown',
            'ip': ip,
            'user_agent': user_agent,
            'timestamp': datetime.now().isoformat()
        }
        self.attempts.append(attempt)
        self.save_data()
        return attempt

lab = AwarenessLab()

# Phishing Detection Engine
class PhishingDetector:
    @staticmethod
    def analyze_url(url):
        """Educational tool to detect phishing indicators"""
        if not url:
            return []
        
        parsed = urlparse(url)
        red_flags = []
        score = 0
        
        # Check 1: IP address instead of domain
        if parsed.netloc.replace('.', '').replace(':', '').isdigit():
            red_flags.append("🚨 CRITICAL: IP address used instead of domain name")
            score += 3
        
        # Check 2: Excessive subdomains
        subdomain_count = parsed.netloc.count('.')
        if subdomain_count > 3:
            red_flags.append(f"⚠️ Suspicious: {subdomain_count} subdomains (unusually high)")
            score += 2
        
        # Check 3: Typosquatting patterns
        suspicious_domains = ['g00gle', 'faceb00k', 'micr0soft', 'appIe', 'amaz0n']
        for suspicious in suspicious_domains:
            if suspicious in parsed.netloc.lower():
                red_flags.append(f"🚨 CRITICAL: Typosquatting detected ({suspicious})")
                score += 3
        
        # Check 4: URL shorteners
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'is.gd', 'buff.ly']
        for shortener in shorteners:
            if shortener in parsed.netloc.lower():
                red_flags.append(f"⚠️ URL shortener used ({shortener}) - hides real destination")
                score += 2
        
        # Check 5: Suspicious keywords
        suspicious_keywords = ['login', 'verify', 'account', 'secure', 'update', 'confirm']
        for keyword in suspicious_keywords:
            if keyword in parsed.path.lower():
                red_flags.append(f"⚠️ Suspicious keyword in URL: '{keyword}'")
                score += 1
        
        # Risk level
        if score >= 5:
            risk = "🔴 HIGH RISK"
        elif score >= 3:
            risk = "🟡 MEDIUM RISK"
        else:
            risk = "🟢 LOW RISK"
        
        return {
            'risk_level': risk,
            'score': score,
            'findings': red_flags,
            'recommendation': "Do NOT enter credentials if you weren't expecting this QR code!"
        }

detector = PhishingDetector()

# Routes
@app.route('/')
def index():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    qr_source = request.args.get('qr', 'false') == 'true'
    
    lab.add_visit(ip, user_agent, qr_source)
    
    return render_template('index.html')

@app.route('/qr-login')
def qr_login():
    """Special route for QR code scans"""
    return redirect(url_for('index', qr='true'))

@app.route('/fake-login', methods=['POST'])
def fake_login():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    email = request.form.get('email', '')
    password = request.form.get('password', '')  # Not stored, just for demo
    
    # Educational logging (no real passwords stored)
    if email:
        lab.add_attempt(email, ip, user_agent)
    
    return redirect(url_for('warning', email=email))

@app.route('/warning')
def warning():
    email = request.args.get('email', 'user')
    
    # Analyze the URL that brought them here
    referer = request.headers.get('Referer', 'Unknown')
    url_analysis = detector.analyze_url(referer)
    
    return render_template('warning.html', 
                         email=email, 
                         url_analysis=url_analysis)

@app.route('/generate-qr')
def generate_qr():
    """Dynamic QR code generator"""
    url = request.args.get('url', 'http://localhost:5000/qr-login')
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64 for embedding
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return jsonify({'qr_code': img_str, 'url': url})

@app.route('/admin/dashboard')
def admin_dashboard():
    """Educational analytics dashboard"""
    # Prepare statistics
    total_visits = len(lab.visits)
    total_attempts = len(lab.attempts)
    
    # Calculate conversion rate
    conversion_rate = (total_attempts / total_visits * 100) if total_visits > 0 else 0
    
    # Time-based analysis
    hourly_data = defaultdict(int)
    for visit in lab.visits:
        hour = datetime.fromisoformat(visit['timestamp']).hour
        hourly_data[hour] += 1
    
    # Domain analysis (which email providers users tried to use)
    domain_counts = defaultdict(int)
    for attempt in lab.attempts:
        domain_counts[attempt['email_domain']] += 1
    
    # Prepare charts using Plotly
    hours = list(range(24))
    visit_counts = [hourly_data[h] for h in hours]
    
    fig1 = go.Figure(data=go.Scatter(x=hours, y=visit_counts, mode='lines+markers'))
    fig1.update_layout(title='QR Scans by Hour', xaxis_title='Hour of Day', yaxis_title='Number of Scans')
    
    # Top domains chart
    top_domains = dict(sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    fig2 = go.Figure(data=go.Bar(x=list(top_domains.keys()), y=list(top_domains.values())))
    fig2.update_layout(title='Email Domains Used', xaxis_title='Domain', yaxis_title='Count')
    
    # Recent activity
    recent_attempts = lab.attempts[-20:][::-1]
    
    return render_template('dashboard.html',
                         total_visits=total_visits,
                         total_attempts=total_attempts,
                         conversion_rate=conversion_rate,
                         chart1_json=json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder),
                         chart2_json=json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder),
                         recent_attempts=recent_attempts)

@app.route('/api/scan-qr-risk')
def scan_qr_risk():
    """API endpoint for QR risk assessment"""
    url = request.args.get('url', '')
    analysis = detector.analyze_url(url)
    return jsonify(analysis)

@app.route('/training-material')
def training_material():
    """Educational resources about QR phishing"""
    return render_template('training.html')

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   🛡️  QR Phishing Awareness Lab - Training Platform  🛡️   ║
    ╠══════════════════════════════════════════════════════════╣
    ║                                                          ║
    ║  📍 Access the lab: http://localhost:5000               ║
    ║  📊 Admin Dashboard: http://localhost:5000/admin/dashboard ║
    ║  📚 Training Material: http://localhost:5000/training-material ║
    ║                                                          ║
    ║  ⚠️  EDUCATIONAL USE ONLY - No real credentials stored  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)