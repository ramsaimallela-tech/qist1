# Deploy AP Grid Quantum Optimiser (GitHub + Streamlit Cloud)

## 1. Push the project to GitHub

### Option A — GitHub website
1. Go to https://github.com/new
2. Create a new repository (e.g. `ap-grid-quantum-optimiser`)
3. Do **not** add a README (you already have one)
4. On your PC, in the project folder:

```powershell
cd "C:\Users\Lakshmitha\OneDrive\Desktop\VS code\FallF"
git init
git add .
git commit -m "AP Grid Quantum Optimiser dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ap-grid-quantum-optimiser.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### Option B — GitHub Desktop
1. File → Add local repository → select the project folder
2. Publish repository to GitHub

---

## 2. Deploy on Streamlit Community Cloud (free)

1. Open https://share.streamlit.io/  
   (sign in with the **same** GitHub account)
2. Click **New app**
3. Fill in:
   - **Repository:** `YOUR_USERNAME/ap-grid-quantum-optimiser`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Advanced settings** → **Secrets** and paste:

```toml
IBM_QUANTUM_TOKEN = "your-real-ibm-api-token"
```

5. Click **Deploy**

After a few minutes you get a public URL like:

`https://ap-grid-quantum-optimiser-xxxxx.streamlit.app`

Share that link — anyone can open the dashboard in a browser.

---

## 3. Local secrets (optional)

For local `streamlit run app.py` with IBM hardware:

```powershell
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
# edit secrets.toml and paste your IBM token
```

Or set an environment variable:

```powershell
$env:IBM_QUANTUM_TOKEN = "your-token"
python -m streamlit run app.py
```

---

## Important notes

| Topic | Detail |
|--------|--------|
| **API key** | Never commit the real token to GitHub. Use Streamlit Secrets or env vars. |
| **IBM jobs** | Real QPU runs can take minutes (queue). Streamlit may show a long spinner; local Aer is always fast. |
| **Free tier** | Streamlit Community Cloud is free for public repos. App sleeps after inactivity; first load can be slow. |
| **Private repo** | Streamlit Cloud supports private repos on paid plans; free plan needs a public repo. |

---

## Quick checklist

- [ ] Code pushed to GitHub
- [ ] `app.py` is the main file
- [ ] `requirements.txt` present
- [ ] IBM token only in Streamlit Secrets (not in source files)
- [ ] Deployed app URL opens in browser
