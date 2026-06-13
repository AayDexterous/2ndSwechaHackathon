import streamlit as st
import requests
import base64
import urllib.parse
import os

st.set_page_config(page_title="Simple Social", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Translation catalogs for English and Hindi
TRANSLATIONS = {
    "en": {
        "login_title": "🚀 Welcome to Simple Social",
        "email": "Email:",
        "password": "Password:",
        "login_btn": "Login",
        "signup_btn": "Sign Up",
        "login_err": "Invalid email or password!",
        "user_info_err": "Failed to get user info",
        "signup_success": "Account created! Click Login now.",
        "signup_err": "Registration failed: {detail}",
        "signup_input_prompt": "Enter your email and password above",
        "upload_title": "📸 Share Something",
        "choose_media": "Choose media",
        "caption": "Caption:",
        "caption_placeholder": "What's on your mind?",
        "share_btn": "Share",
        "uploading": "Uploading...",
        "posted": "Posted!",
        "upload_err": "Upload failed!",
        "feed_title": "🏠 Feed",
        "no_posts": "No posts yet! Be the first to share something.",
        "post_deleted": "Post deleted!",
        "delete_err": "Failed to delete post!",
        "feed_err": "Failed to load feed",
        "hi_user": "👋 Hi {email}!",
        "logout": "Logout",
        "navigate": "Navigate:",
        "nav_feed": "🏠 Feed",
        "nav_upload": "📸 Upload",
    },
    "hi": {
        "login_title": "🚀 सिंपल सोशल में आपका स्वागत है",
        "email": "ईमेल:",
        "password": "पासवर्ड:",
        "login_btn": "लॉग इन",
        "signup_btn": "साइन अप",
        "login_err": "अमान्य ईमेल या पासवर्ड!",
        "user_info_err": "उपयोगकर्ता की जानकारी प्राप्त करने में विफल",
        "signup_success": "खाता बन गया! अब लॉग इन करें।",
        "signup_err": "पंजीकरण विफल: {detail}",
        "signup_input_prompt": "ऊपर अपना ईमेल और पासवर्ड दर्ज करें",
        "upload_title": "📸 कुछ साझा करें",
        "choose_media": "मीडिया चुनें",
        "caption": "कैप्शन:",
        "caption_placeholder": "आपके मन में क्या है?",
        "share_btn": "साझा करें",
        "uploading": "अपलोड हो रहा है...",
        "posted": "साझा कर दिया गया!",
        "upload_err": "अपलोड विफल रहा!",
        "feed_title": "🏠 फ़ीड",
        "no_posts": "अभी तक कोई पोस्ट नहीं है! कुछ साझा करने वाले पहले व्यक्ति बनें।",
        "post_deleted": "पोस्ट हटा दी गई!",
        "delete_err": "पोस्ट हटाने में विफल!",
        "feed_err": "फ़ीड लोड करने में विफल",
        "hi_user": "👋 नमस्ते {email}!",
        "logout": "लॉग आउट",
        "navigate": "नेविगेट करें:",
        "nav_feed": "🏠 फ़ीड",
        "nav_upload": "📸 अपलोड",
    }
}

# Initialize session state variables
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'lang' not in st.session_state:
    st.session_state.lang = "en"

# Display a language toggle selectbox at the top right corner
col_spacer, col_lang = st.columns([5, 1.2])
with col_lang:
    selected_lang = st.selectbox(
        "🌐 Language / भाषा",
        ["English", "हिंदी"],
        index=0 if st.session_state.lang == "en" else 1,
        key="lang_selector"
    )
    st.session_state.lang = "en" if selected_lang == "English" else "hi"

lang = st.session_state.lang


def get_headers():
    """Get authorization headers with token"""
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def login_page():
    st.title(TRANSLATIONS[lang]["login_title"])

    # Simple form with two buttons
    email = st.text_input(TRANSLATIONS[lang]["email"])
    password = st.text_input(TRANSLATIONS[lang]["password"], type="password")

    if email and password:
        col1, col2 = st.columns(2)

        with col1:
            if st.button(TRANSLATIONS[lang]["login_btn"], type="primary", use_container_width=True):
                # Login using FastAPI Users JWT endpoint
                login_data = {"username": email, "password": password}
                response = requests.post(f"{BACKEND_URL}/auth/jwt/login", data=login_data)

                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data["access_token"]

                    # Get user info
                    user_response = requests.get(f"{BACKEND_URL}/users/me", headers=get_headers())
                    if user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.rerun()
                    else:
                        st.error(TRANSLATIONS[lang]["user_info_err"])
                else:
                    st.error(TRANSLATIONS[lang]["login_err"])

        with col2:
            if st.button(TRANSLATIONS[lang]["signup_btn"], type="secondary", use_container_width=True):
                # Register using FastAPI Users
                signup_data = {"email": email, "password": password}
                response = requests.post(f"{BACKEND_URL}/auth/register", json=signup_data)

                if response.status_code == 201:
                    st.success(TRANSLATIONS[lang]["signup_success"])
                else:
                    error_detail = response.json().get("detail", "Registration failed")
                    st.error(TRANSLATIONS[lang]["signup_err"].format(detail=error_detail))
    else:
        st.info(TRANSLATIONS[lang]["signup_input_prompt"])


def upload_page():
    st.title(TRANSLATIONS[lang]["upload_title"])

    uploaded_file = st.file_uploader(TRANSLATIONS[lang]["choose_media"], type=['png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'mkv', 'webm'])
    caption = st.text_area(TRANSLATIONS[lang]["caption"], placeholder=TRANSLATIONS[lang]["caption_placeholder"])

    if uploaded_file and st.button(TRANSLATIONS[lang]["share_btn"], type="primary"):
        with st.spinner(TRANSLATIONS[lang]["uploading"]):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"caption": caption}
            response = requests.post(f"{BACKEND_URL}/upload", files=files, data=data, headers=get_headers())

            if response.status_code == 200:
                st.success(TRANSLATIONS[lang]["posted"])
                st.rerun()
            else:
                st.error(TRANSLATIONS[lang]["upload_err"])


def encode_text_for_overlay(text):
    """Encode text for ImageKit overlay - base64 then URL encode"""
    if not text:
        return ""
    # Base64 encode the text
    base64_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    # URL encode the result
    return urllib.parse.quote(base64_text)


def create_transformed_url(original_url, transformation_params, caption=None):
    if caption:
        encoded_caption = encode_text_for_overlay(caption)
        # Add text overlay at bottom with semi-transparent background
        text_overlay = f"l-text,ie-{encoded_caption},ly-N20,lx-20,fs-100,co-white,bg-000000A0,l-end"
        transformation_params = text_overlay

    if not transformation_params:
        return original_url

    parts = original_url.split("/")

    imagekit_id = parts[3]
    file_path = "/".join(parts[4:])
    base_url = "/".join(parts[:4])
    return f"{base_url}/tr:{transformation_params}/{file_path}"


def feed_page():
    st.title(TRANSLATIONS[lang]["feed_title"])

    response = requests.get(f"{BACKEND_URL}/feed", headers=get_headers())
    if response.status_code == 200:
        posts = response.json()["posts"]

        if not posts:
            st.info(TRANSLATIONS[lang]["no_posts"])
            return

        for post in posts:
            st.markdown("---")

            # Header with user, date, and delete button (if owner)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{post['email']}** • {post['created_at'][:10]}")
            with col2:
                if post.get('isowner', False):
                    if st.button("🗑️", key=f"delete_{post['id']}", help="Delete post"):
                        # Delete the post
                        response = requests.delete(f"{BACKEND_URL}/posts/{post['id']}", headers=get_headers())
                        if response.status_code == 200:
                            st.success(TRANSLATIONS[lang]["post_deleted"])
                            st.rerun()
                        else:
                            st.error(TRANSLATIONS[lang]["delete_err"])

            # Uniform media display with caption overlay
            caption = post.get('caption', '')
            if post['file_type'] == 'image':
                uniform_url = create_transformed_url(post['url'], "", caption)
                st.image(uniform_url, width=300)
            else:
                # For videos: specify only height to maintain aspect ratio + caption overlay
                uniform_video_url = create_transformed_url(post['url'], "w-400,h-200,cm-pad_resize,bg-blurred")
                st.video(uniform_video_url, width=300)
                st.caption(caption)

            st.markdown("")  # Space between posts
    else:
        st.error(TRANSLATIONS[lang]["feed_err"])


# Main app logic
if st.session_state.user is None:
    login_page()
else:
    # Sidebar navigation
    welcome_text = TRANSLATIONS[lang]["hi_user"].format(email=st.session_state.user['email'])
    st.sidebar.title(welcome_text)

    if st.sidebar.button(TRANSLATIONS[lang]["logout"]):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    st.sidebar.markdown("---")
    
    # Track selection index to prevent reset when changing languages
    if 'selected_idx' not in st.session_state:
        st.session_state.selected_idx = 0
        
    nav_feed_str = TRANSLATIONS[lang]["nav_feed"]
    nav_upload_str = TRANSLATIONS[lang]["nav_upload"]
    
    page = st.sidebar.radio(
        TRANSLATIONS[lang]["navigate"],
        [nav_feed_str, nav_upload_str],
        index=st.session_state.selected_idx
    )
    
    # Update index in session state
    st.session_state.selected_idx = 0 if page == nav_feed_str else 1

    if page == nav_feed_str:
        feed_page()
    else:
        upload_page()