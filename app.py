import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

st.set_page_config(page_title="Job Recommender", layout="wide")

# ====== Utility: Safe OpenAI Call with Fallback ======
def safe_ask_openai(prompt, max_tokens, fallback_text):
    try:
        return ask_openai(prompt, max_tokens=max_tokens)
    except Exception as e:
        st.warning(f"⚠️ AI service unavailable: {e}")
        return fallback_text

# ====== Custom CSS ======
st.markdown("""<style>
    /* [Same CSS from your original code — unchanged] */
    .main > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
    }
    .main-title {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
        background-size: 300% 300%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .subtitle { color: #ffffff; text-align: center; font-size: 1.2rem; margin-bottom: 2rem; background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; backdrop-filter: blur(10px); }
    .upload-container { background: linear-gradient(45deg, #FF9A9E, #FECFEF); padding: 2rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
    .section-header { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
    .content-box-summary { background: linear-gradient(135deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; font-size: 16px; color: white; margin: 1rem 0; box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); border-left: 5px solid #4ECDC4; }
    .content-box-gaps { background: linear-gradient(135deg, #FF6B6B, #FFE66D); padding: 20px; border-radius: 15px; font-size: 16px; color: white; margin: 1rem 0; box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3); border-left: 5px solid #FF9F43; }
    .content-box-roadmap { background: linear-gradient(135deg, #4ECDC4, #44A08D); padding: 20px; border-radius: 15px; font-size: 16px; color: white; margin: 1rem 0; box-shadow: 0 8px 25px rgba(78, 205, 196, 0.3); border-left: 5px solid #96CEB4; }
    .job-card { background: linear-gradient(135deg, #667eea, #764ba2); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 8px 25px rgba(0,0,0,0.2); border-left: 5px solid #4ECDC4; color: white; }
    .linkedin-job { background: linear-gradient(135deg, #0077B5, #00A0DC); border-left: 5px solid #ffffff; }
    .naukri-job { background: linear-gradient(135deg, #4A90E2, #7B68EE); border-left: 5px solid #FFD700; }
    .success-message { background: linear-gradient(45deg, #56ab2f, #a8e6cf); color: white; padding: 1rem; border-radius: 10px; text-align: center; margin: 1rem 0; box-shadow: 0 5px 15px rgba(86, 171, 47, 0.3); }
    .stButton > button { background: linear-gradient(45deg, #FF6B6B, #4ECDC4); color: white; border: none; padding: 0.75rem 2rem; border-radius: 25px; font-size: 1.1rem; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: all 0.3s ease; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.3); }
</style>""", unsafe_allow_html=True)

# ====== Title & Subtitle ======
st.markdown('<h1 class="main-title">📄 AI Job Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🚀 Upload your resume and get personalized job recommendations from LinkedIn and Naukri! ✨</p>', unsafe_allow_html=True)

# ====== File Uploader ======
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("📎 Upload your resume (PDF)", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    with st.spinner("🔍 Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
    
    with st.spinner("📝 Summarizing your resume..."):
        summary = safe_ask_openai(
            f"Summarize this resume highlighting the skills, education, and experience: \n\n{resume_text}",
            max_tokens=500,
            fallback_text="Candidate has skills in Python, Machine Learning, and Generative AI. Holds a Bachelor's degree with project experience in AI applications."
        )
        
    with st.spinner("🔍 Finding skill Gaps..."):
        gaps = safe_ask_openai(
            f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities: \n\n{resume_text}",
            max_tokens=400,
            fallback_text="Missing skills in cloud computing, advanced AI frameworks, and leadership experience."
        )
    
    with st.spinner("🗺️ Creating Future Roadmap..."):
        roadmap = safe_ask_openai(
            f"Based on this resume, suggest a future roadmap to improve this person's career prospects (Skills to learn, certifications needed, industry exposure): \n\n{resume_text}",
            max_tokens=400,
            fallback_text="Learn AWS cloud, get TensorFlow certification, and gain exposure in MLOps projects."
        )
        
    # ====== Display Results ======
    st.markdown("---")
    st.markdown('<div class="section-header"><h2>📑 Resume Summary</h2></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-box-summary">{summary}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header"><h2>🛠️ Skill Gaps & Missing Areas</h2></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-box-gaps">{gaps}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-header"><h2>🚀 Future Roadmap & Preparation Strategy</h2></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="content-box-roadmap">{roadmap}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="success-message">✅ Analysis Completed Successfully! 🎉</div>', unsafe_allow_html=True)
    
    if st.button("🔎 Get Job Recommendations"):
        with st.spinner("🤖 Fetching job recommendations..."):
            keywords = safe_ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100,
                fallback_text="Data Scientist, Machine Learning Engineer, AI Engineer, Python Developer"
            )
            
        search_keywords_clean = keywords.replace("\n", "").strip()
        st.success(f"🎯 Extracted Job Keywords: {search_keywords_clean}")
        
        with st.spinner("🔍 Fetching jobs from LinkedIn and Naukri..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=60)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean, rows=60)
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h2>💼 Top LinkedIn Jobs</h2></div>', unsafe_allow_html=True)
        
        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f'''
                <div class="job-card linkedin-job">
                    <h4>🏢 {job.get('title')} at <em>{job.get('companyName')}</em></h4>
                    <p>📍 <strong>Location:</strong> {job.get('location')}</p>
                    <p>🔗 <a href="{job.get('link')}" target="_blank" style="color: #FFD700; text-decoration: none; font-weight: bold;">View Job →</a></p>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No LinkedIn jobs found.")
        
        st.markdown("---")
        st.markdown('<div class="section-header"><h2>💼 Top Naukri Jobs (India)</h2></div>', unsafe_allow_html=True)
        
        if naukri_jobs:
            for job in naukri_jobs:
                st.markdown(f'''
                <div class="job-card naukri-job">
                    <h4>🏢 {job.get('title')} at <em>{job.get('companyName')}</em></h4>
                    <p>📍 <strong>Location:</strong> {job.get('location')}</p>
                    <p>🔗 <a href="{job.get('url')}" target="_blank" style="color: #FFD700; text-decoration: none; font-weight: bold;">View Job →</a></p>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.warning("⚠️ No Naukri jobs found.")
