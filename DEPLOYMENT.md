# Streamlit Deployment Guide

## Quick Start

### Option 1: Run Locally (Simplest)

```bash
# Using the helper script
chmod +x run_app.sh
./run_app.sh

# OR manually
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens at: **http://localhost:8501**

---

## Cloud Deployment Options

### 🌟 Option 1: Streamlit Cloud (Recommended for Beginners)

**Pros:** Free, easy, no infrastructure needed  
**Cons:** Limited resources

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Click **"New app"**

4. Fill in:
   - GitHub repo: `gk0356743-collab/minor-project-2`
   - Branch: `main`
   - File path: `streamlit_app.py`

5. Click **"Deploy"** ✓

Your app will be live in 2-3 minutes!

---

### 🐳 Option 2: Docker (All Platforms)

**Pros:** Works everywhere, consistent environment  
**Cons:** Requires Docker installation

#### Create Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run:

```bash
# Build image
docker build -t student-marks-app .

# Run container
docker run -p 8501:8501 student-marks-app

# Or run in background
docker run -d -p 8501:8501 --name student-app student-marks-app
```

Access at: **http://localhost:8501**

---

### ☁️ Option 3: Render (Free Tier Available)

1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Create new **Web Service**
4. Connect GitHub repo
5. Build command: `pip install -r requirements.txt`
6. Start command: `streamlit run streamlit_app.py --server.port=8501`
7. Add environment variable: `STREAMLIT_SERVER_HEADLESS=true`
8. Deploy

---

### 🚀 Option 4: Heroku (Paid)

1. Create Procfile:
   ```bash
   echo "web: streamlit run streamlit_app.py" > Procfile
   ```

2. Deploy:
   ```bash
   heroku login
   heroku create student-marks-app
   git push heroku main
   ```

---

### 🌐 Option 5: AWS EC2

1. Launch Ubuntu instance
2. SSH into instance
3. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   ```
4. Run app:
   ```bash
   streamlit run streamlit_app.py --server.address 0.0.0.0
   ```
5. Access via public IP

---

### 🔵 Option 6: Google Cloud Platform

1. Install Cloud CLI
2. Deploy:
   ```bash
   gcloud app deploy
   ```
3. Requires `app.yaml`:
   ```yaml
   runtime: python39
   env: standard
   entrypoint: streamlit run streamlit_app.py --server.port 8080 --server.address 0.0.0.0
   ```

---

### 💜 Option 7: PythonAnywhere

1. Upload files
2. Set up virtual environment
3. Configure WSGI file
4. Access via provided URL

---

## Environment Variables

Create `.env` file for sensitive data:

```
DATA_PATH=data/student_marks.csv
STREAMLIT_THEME_PRIMARYCOLOR=#0066ff
STREAMLIT_THEME_BACKGROUNDCOLOR=#ffffff
```

---

## Performance Tips

1. **Cache data loading:**
   ```python
   @st.cache_data
   def load_data():
       return pd.read_csv('data/student_marks.csv')
   ```

2. **Optimize visualizations** - Use plotly for faster rendering

3. **Minimize file size** - Keep CSV under 10MB for free tier

4. **Use CDN** - For images and assets

---

## Troubleshooting

### App won't start
```bash
streamlit run streamlit_app.py --logger.level=debug
```

### Port already in use
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Missing dependencies
```bash
pip install -r requirements.txt --upgrade
```

### CSV file not found
- Ensure `data/student_marks.csv` exists
- Check file path is relative to app location

---

## Monitoring & Logs

**Streamlit Cloud:**
- View logs in dashboard
- Check email for alerts

**Docker:**
```bash
docker logs student-app
```

**Local:**
```bash
streamlit run streamlit_app.py --logger.level=info
```

---

## Security Best Practices

1. ✓ Use `.gitignore` for sensitive files
2. ✓ Environment variables for secrets
3. ✓ Don't commit API keys
4. ✓ Enable HTTPS in production
5. ✓ Validate user inputs

---

## Next Steps

- Add authentication (Streamlit Cloud supports OAuth)
- Add more data sources
- Implement download reports feature
- Add database integration
- Create admin dashboard

---

For questions or issues, refer to [Streamlit Documentation](https://docs.streamlit.io)
