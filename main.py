import os
import firebase_admin
from firebase_admin import credentials, firestore
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.text import LabelBase
from kivy.properties import StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.color_definitions import colors 
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem 
from kivymd.uix.button import MDRaisedButton, MDTextButton, MDFloatingActionButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
import webbrowser
from kivymd.uix.card import MDCard
import datetime
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.fitimage import FitImage
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
import random
from kivy.clock import Clock
from kivy.factory import Factory
import requests
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIREBASE_WEB_API_KEY = "KEY"
APP_ID = "kalaatokri-51ed2"

KV = '''
#:set PADDING dp(10)

ScreenManager:
    SplashScreen:
    LoginScreen:
    HomeScreen:
    WorkshopDetailScreen:
    GalleryDetailScreen:

<SplashScreen>:
    name: "splash"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(40)
        spacing: dp(20)
        MDLabel:
            text: "Kalaatokri"
            halign: "center"
            font_name: "ChelseaMarket"
            font_size: "50sp"
            theme_text_color: "Primary"
        MDRaisedButton:
            text: "Continue"
            pos_hint: {"center_x": 0.5}
            on_release: root.manager.current = "login"

<LoginScreen>:
    name: "login"
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(40)
        spacing: dp(20)
        MDLabel:
            text: "Welcome to Kalaatokri"
            halign: "center"
            font_name: "ChelseaMarket"
            font_size: "30sp"
            theme_text_color: "Primary"

        MDTextField:
            id: username 
            hint_text: "Choose a username"
            icon_right: "account"
            
        MDTextField:
            id: email
            hint_text: "Enter g-mail"
        MDTextField:
            id: password
            hint_text: "Enter password"
            password: True
        MDRaisedButton:
            text: "Login"
            pos_hint: {"center_x": 0.5}
            on_release: app.login(email.text, password.text)
        MDRaisedButton:
            text: "Register"
            pos_hint: {"center_x": 0.5}
            # Update the on_release to include the username field
            on_release: app.register(username.text, email.text, password.text)
        MDTextButton:
            text: "Quick Demo (No Login)"
            pos_hint: {"center_x": 0.5}
            on_release: app.demo_login()

<HomeScreen>:
    name: "home"
    MDBoxLayout:
        orientation: "vertical"
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: app.theme_cls.primary_color
            padding: PADDING
            MDLabel:
                text: "Kalaatokri"
                halign: 'left'
                font_name: "ChelseaMarket"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        
        MDBottomNavigation:
            id: bottom_nav
            on_switch_tabs: app.on_tab_switch(*args)
            WorkshopsPage:
            GalleryPage:
            ProfilePage:

<WorkshopsPage>:
    name: "workshops_page"
    text: "Workshops"
    icon: "palette"
    FloatLayout:
        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                spacing: PADDING
                padding: PADDING
                size_hint_y: None
                height: self.minimum_height
                WorkshopCard:
                    workshop_name: "Abstract Art Painting Workshop"
                    image: app.asset_path("assets/abstractart_workshop.png")
                WorkshopCard:
                    workshop_name: "Art Therapy Session (Non-Clinical)"
                    image: app.asset_path("assets/arttherapy_workshop.png")
                WorkshopCard:
                    workshop_name: "Balloon Art Class"
                    image: app.asset_path("assets/balloonart_workshop.png")
                WorkshopCard:
                    workshop_name: "Soap Making Workshop"
                    image: app.asset_path("assets/soap_workshop.png")
                MDRaisedButton:
                    text: "Open Workshops Website"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.open_link("https://www.kalaatokri.com/")
        MDFloatingActionButton:
            id: fab_main
            icon: "plus"
            pos: dp(20), dp(20)
            on_release: root.toggle_fabs()
        MDFloatingActionButton:
            id: fab_insta
            icon: "instagram"
            pos: dp(20), dp(90)
            opacity: 0
            on_release: app.open_link("https://instagram.com/kalaatokri")
        MDFloatingActionButton:
            id: fab_yt
            icon: "youtube"
            pos: dp(20), dp(160)
            opacity: 0
            on_release: app.open_link("https://www.youtube.com/@mycraftareaalifestyle")
        MDFloatingActionButton:
            id: fab_amazon
            icon: "book-open-variant"
            pos: dp(20), dp(230)
            opacity: 0
            on_release: app.open_link("https://www.amazon.in/dp/B0CDG8R5J9?ref=cm_sw_r_ffobk_cp_ud_dp_JEE4SW1RD4C0M7PFH5YA&ref_=cm_sw_r_ffobk_cp_ud_dp_JEE4SW1RD4C0M7PFH5YA&social_share=cm_sw_r_ffobk_cp_ud_dp_JEE4SW1RD4C0M7PFH5YA&bestFormat=true")
        MDFloatingActionButton:
            id: fab_pinterest
            icon: "pinterest"
            pos: dp(20), dp(300)
            opacity: 0
            on_release: app.open_link("https://in.pinterest.com/kalaatokri/")

<GalleryPage>:
    name: "gallery_page"
    text: "Gallery"
    icon: "image"
    ScrollView:
        GridLayout:
            cols: 2
            spacing: PADDING
            padding: PADDING
            size_hint_y: None
            height: self.minimum_height
            
            GalleryImage:
                source: app.asset_path("assets/whim.png")
                description: "Let your imagination roam free with whimsical art and bursts of vibrant color. Each playful line and bold hue lifts your spirit and quiets the mind. There are no rules—just joy, curiosity, and creative freedom. In this colorful world, relaxation and wonder go hand in hand."
            GalleryImage:
                source: app.asset_path("assets/colorT.png")
                description: "Feel your stress/tension fade as calming colours flow through your fingertips. With each stroke, color therapy gently balances your emotions and mind. Let the hues guide you to a peaceful, creative sanctuary within."
            GalleryImage:
                source: app.asset_path("assets/geo_abs.png")
                description: "Find calm in the rhythm of lines, shapes, and patterns as you explore geometrical abstract art. The balance of symmetry and color becomes a peaceful meditation in motion. Each design is a quiet expression of order and creativity. Let structure and spontaneity guide you to a relaxed, centered state."
            GalleryImage:
                source: app.asset_path("assets/block_p.png")
                description: "Block printing offers a peaceful rhythm that quiets the mind and awakens creativity. The repetitive press of carved blocks and the gentle flow of ink bring a calming sense of focus. Each print becomes a mindful moment, grounding you in the beauty of handmade simplicity."
            GalleryImage:
                source: app.asset_path("assets/landscape.png")
                description: "Creating colourful landscapes is a soothing therapy that reflects the emotions and state of mind within. As each hue blends into the next, it brings clarity, calm, and a gentle release of inner thoughts. This mindful process transforms your canvas into a peaceful escape and your mind into a place of quiet harmony."
            GalleryImage:
                source: app.asset_path("assets/fluid.png")
                description: "Let go and flow with the soothing movement of fluid art and Dutch pour techniques. Watch colors dance and swirl, blending effortlessly in a calming, creative release. There's beauty in the unexpected, where every pour brings a moment of mindfulness. Relax, unwind, and let the paint carry your stress away."
            GalleryImage:
                source: app.asset_path("assets/decoupage.png")
                description: "Unwind your mind as you immerse yourself in the soothing rhythm of decoupage. Let each cut, glue, and brushstroke melt away the stress of the day. This calming craft turns quiet moments into beautiful, artful escapes."
            GalleryImage:
                source: app.asset_path("assets/madhubani.png")
                description: "Immerse yourself in the soothing rhythm of Madhubani painting, where each intricate stroke connects you to centuries of tradition. Using natural colors derived from plants and flowers, this mindful art form calms the mind and uplifts the spirit. As the pigments flow, so does a sense of peace, turning every moment into a meditative journey."
            GalleryImage:
                source: app.asset_path("assets/free_flow.png")
                description: "Experience the calming joy of painting florals with watercolours, letting each brushstroke flow freely without the constraints of a sketch. This intuitive technique encourages mindfulness, spontaneity, and self-expression. As colours blend and bloom on the paper, stress melts away, leaving behind a serene floral dance."
                   
<ProfilePage>:
    name: "profile_page"
    text: "Profile"
    icon: "account-cog" 

    ScrollView:
        MDList:
            OneLineListItem:
                text: f"Hi, {app.current_user_name}!"
                font_style: "H6"
                disabled: True

            OneLineAvatarIconListItem:
                text: "Delete My Account"
                on_release: app.confirm_delete_account()
                
                IconLeftWidget:
                    icon: "delete-forever"
                    theme_text_color: "Error"

            OneLineAvatarIconListItem:
                text: "About Kalaatokri"
                on_release: app.show_about_dialog()
                
                IconLeftWidget:
                    icon: "information-outline"

            OneLineAvatarIconListItem:
                text: "Send Feedback"
                on_release: app.send_feedback()
                
                IconLeftWidget:
                    icon: "email-send-outline"
            
            OneLineAvatarIconListItem:
                text: f"Version {app.version}"
                disabled: True
                
                IconLeftWidget:
                    icon: "cellphone-information"
            
            OneLineAvatarIconListItem:
                text: "FAQ"
                on_release: app.show_faq_dialog()
                
                IconLeftWidget:
                    icon: "help-circle-outline"

<WorkshopDetailScreen>:
    name: "workshop_detail"
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: app.theme_cls.primary_color
            padding: dp(4)
            MDIconButton:
                icon: 'arrow-left'
                on_release: app.go_home()
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDLabel:
                text: root.workshop_name
                font_name: "ChelseaMarket"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        FitImage:
            source: app.asset_path(root.image) if root.image else ""
            size_hint_y: None
            height: dp(200)
        ScrollView:
            MDBoxLayout:
                id: comments_box
                orientation: 'vertical'
                adaptive_height: True
                padding: PADDING
                spacing: PADDING
        MDBoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: PADDING
            spacing: PADDING
            MDTextField:
                id: comment_input
                hint_text: "Add a comment..."
            MDRaisedButton:
                text: "Post"
                on_release: app.add_comment(root.workshop_name, comment_input.text)

<GalleryDetailScreen>:
    name: "gallery_detail"
    MDBoxLayout:
        orientation: 'vertical'
        MDBoxLayout:
            size_hint_y: None
            height: dp(56)
            md_bg_color: app.theme_cls.primary_color
            padding: dp(4)
            MDIconButton:
                icon: 'arrow-left'
                on_release: app.go_home()
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDLabel:
                text: "Gallery"
                font_name: "ChelseaMarket"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(20)
                FitImage:
                    id: gallery_image
                    size_hint_y: None
                    height: dp(250)
                MDLabel:
                    id: gallery_text
                    halign: 'center'
                    theme_text_color: "Primary"
                    adaptive_height: True

<GalleryImage@ButtonBehavior+FitImage>:
    description: ""
    size_hint_y: None
    height: dp(150)
    on_release: app.show_gallery(self.source, self.description)

<WorkshopCard@MDCard+ButtonBehavior>:
    workshop_name: ""
    image: ""
    orientation: "vertical"
    size_hint_y: None
    height: dp(200)
    radius: [20,]
    on_release: app.open_workshop(root.workshop_name, root.image)
    FitImage:
        source: app.asset_path(root.image) if root.image else ""
        radius: [20, 20, 0, 0]
    MDBoxLayout:
        size_hint_y: None
        height: dp(40)
        md_bg_color: 0, 0, 0, 0.5
        padding: PADDING
        Label:
            text: root.workshop_name
            font_name: "ChelseaMarket"
            color: 1, 1, 1, 1

<CommentWidget@MDBoxLayout>:
    orientation: "vertical"
    padding: PADDING
    spacing: dp(5)
    adaptive_height: True
    comment_id: ""
    username: ""

    MDBoxLayout:
        orientation: "horizontal"
        spacing: PADDING
        size_hint_y: None
        height: dp(40)
        Image:
            id: profile_image
            source: ""
            size_hint: None, None
            size: dp(40), dp(40)
        MDBoxLayout:
            orientation: "vertical"
            MDLabel:
                id: username_label
                text: "Username"
                bold: True
                font_name: "ChelseaMarket"
                theme_text_color: "Primary"
            MDLabel:
                id: timestamp_label
                text: "timestamp"
                font_style: "Caption"
                theme_text_color: "Secondary"

    MDLabel:
        id: message_label
        text: "Message"
        adaptive_height: True
        theme_text_color: "Primary"
        
    MDBoxLayout:
        adaptive_height: True
        padding: 0, dp(5)
        MDTextButton:
            text: "Reply"
            on_release: app.reply_to_comment(root.username)

        MDIconButton:
            icon: "delete"
            opacity: 1 if app.is_admin else 0
            disabled: not app.is_admin
            on_release: app.delete_comment(app.root.get_screen('workshop_detail').workshop_name, root.comment_id)
        
'''

class SplashScreen(Screen): pass
class LoginScreen(Screen): pass
class HomeScreen(Screen): pass
class ProfilePage(MDBottomNavigationItem): pass
class WorkshopDetailScreen(Screen):
    workshop_name = StringProperty("")
    image = StringProperty("")
class GalleryDetailScreen(Screen): pass
class WorkshopsPage(MDBottomNavigationItem):
    def toggle_fabs(self):
        try:
            state = self.ids.fab_insta.opacity
            new_opacity = 1 if state == 0 else 0
            
            self.ids.fab_insta.opacity = new_opacity
            self.ids.fab_yt.opacity = new_opacity
            self.ids.fab_amazon.opacity = new_opacity   
            self.ids.fab_pinterest.opacity = new_opacity 
        except Exception as e:
            print(f"FAB toggle error: {e}")
class GalleryPage(MDBottomNavigationItem): pass

class MainApp(MDApp):
    # --- Properties ---
    current_user_id = StringProperty(None)
    current_user_name = StringProperty("Anonymous")
    id_token = StringProperty(None)
    is_admin = BooleanProperty(False)
    version = StringProperty("1.0.0")
    dialog = None
    
    # --- Build Method ---
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"
        try:
            LabelBase.register(
                name="ChelseaMarket", 
                fn_regular=self.asset_path("assets/fonts/ChelseaMarket-Regular.ttf")
            )
        except Exception as e:
            print(f"Font file not found: {e}.")
        return Builder.load_string(KV)

    # --- Core App Logic ---
    def on_tab_switch(self, *args):
        pass

    def asset_path(self, relative_path):
        full_path = os.path.join(BASE_DIR, relative_path)
        if not os.path.exists(full_path):
            print(f"ERROR: File does not exist at path: {full_path}") 
        return full_path

    # --- Authentication (Secure) ---
    def login(self, email, password):
        if not email or not password:
            return self.show_dialog("Error", "Please enter both email and password")
        
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        payload = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        
        try:
            response = requests.post(rest_api_url, data=payload)
            if response.ok:
                response_data = response.json()
                self.current_user_id = response_data['localId']
                self.id_token = response_data['idToken']
                
                print(f"DEBUG: Login successful for UID: {self.current_user_id}") # <-- ADD THIS
                
                self.fetch_user_profile()
                self.root.current = "home"
            else:
                self.show_dialog("Login Failed", "Invalid email or password.")
        except requests.exceptions.RequestException:
            self.show_dialog("Connection Error", "Could not connect to server.")


    def register(self, username, email, password):
        if not username.strip(): return self.show_dialog("Error", "Please enter a username.")
        if not email or not password or len(password) < 6: return self.show_dialog("Error", "Enter valid email and a password of at least 6 characters.")
        
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
        payload = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        
        try:
            response = requests.post(rest_api_url, data=payload)
            if not response.ok: return self.show_dialog("Error", "Registration failed. The email may already be in use.")

            response_data = response.json()
            user_id = response_data['localId']
            self.id_token = response_data['idToken']
            
            profile_data = {
                'fields': {
                    'username': {'stringValue': username},
                    'email': {'stringValue': email},
                    'role': {'stringValue': 'user'}
                }
            }
            requests.patch(
                f"https://firestore.googleapis.com/v1/projects/{APP_ID}/databases/(default)/documents/users/{user_id}",
                params={'auth': self.id_token},
                json=profile_data
            )
            self.show_dialog("Success", "Registration successful! You can now log in.")
        except requests.exceptions.RequestException:
            self.show_dialog("Connection Error", "Could not connect to server.")

    def logout(self):
        self.current_user_id = None
        self.current_user_name = "Anonymous"
        self.id_token = None
        self.is_admin = False
        self.root.current = "login"

    def demo_login(self):
        self.current_user_id = "demo_user_" + str(random.randint(1000, 9999))
        self.current_user_name = "DemoUser"
        self.is_admin = False 
        self.root.current = "home"
    
    def fetch_user_profile(self):
        if not self.id_token: return
        
        url = f"https://firestore.googleapis.com/v1/projects/{APP_ID}/databases/(default)/documents/users/{self.current_user_id}"
        
        try:
            response = requests.get(url, params={'auth': self.id_token})
            
            if response.ok:
                data = response.json().get('fields', {})
                self.current_user_name = data.get('username', {}).get('stringValue', 'Unknown')
                self.is_admin = data.get('role', {}).get('stringValue') == 'admin'
            else:
                print(f"DEBUG: Profile fetch failed. Response: {response.text}")
                self.is_admin = False
        except requests.exceptions.RequestException:
            self.current_user_name = "Network Error"

    # --- Workshop Comments (Secure) ---
    def open_workshop(self, name, image):
        detail_screen = self.root.get_screen("workshop_detail")
        detail_screen.workshop_name = name
        detail_screen.image = image
        self.load_workshop_comments(name) # This now calls the secure version
        self.root.current = "workshop_detail"
        
    # In your MainApp class
    def load_workshop_comments(self, workshop_name):
        if not self.id_token and self.current_user_id != "demo_user_": return

        collection_id = f'workshop_comments_{workshop_name.replace(" ", "_")}'
        parent_path = f'projects/{APP_ID}/databases/(default)/documents/artifacts/{APP_ID}/public/data'
        url = f"https://firestore.googleapis.com/v1/{parent_path}:runQuery"
        
        query_data = {
            "structuredQuery": {
                "from": [{"collectionId": collection_id}],
                "orderBy": [{"field": {"fieldPath": "timestamp"}, "direction": "ASCENDING"}],
                "limit": 50
            }
        }
        
        # --- THIS IS THE FIX ---
        # For POST requests, authentication must be in the headers
        headers = {"Authorization": f"Bearer {self.id_token}"}
        
        try:
            # Note: `params` is removed, and `headers` is added
            response = requests.post(url, headers=headers, json=query_data)
            
            if response.ok:
                self._update_comments_ui(response.json())
            else:
                print(f"Error fetching comments: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Connection error fetching comments: {e}")

    def _update_comments_ui(self, documents):
        try:
            comments_box = self.root.get_screen("workshop_detail").ids.comments_box
            comments_box.clear_widgets()
            
            for doc in documents:
                if 'document' not in doc: continue
                
                comment_id = doc['document']['name'].split('/')[-1]
                fields = doc['document'].get('fields', {})
                
                username = fields.get('username', {}).get('stringValue', '...')
                message = fields.get('message', {}).get('stringValue', '')
                timestamp_str = fields.get('timestamp', {}).get('timestampValue', '')
                timestamp = datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) if timestamp_str else datetime.datetime.now()
                
                self.create_comment_widget(comment_id, username, message, timestamp, comments_box)
        except Exception as e:
            print(f"Error updating comments UI: {e}")

    def add_comment(self, workshop_name, text):
        if not text.strip(): return
        if not self.id_token and self.current_user_id != "demo_user_":
             return self.show_dialog("Login Required", "You must be logged in to comment.")

        collection_path = f'artifacts/{APP_ID}/public/data/workshop_comments_{workshop_name.replace(" ", "_")}'
        url = f"https://firestore.googleapis.com/v1/projects/{APP_ID}/databases/(default)/documents/{collection_path}"
        
        post_data = {
            'fields': {
                'username': {'stringValue': self.current_user_name},
                'message': {'stringValue': text},
                'timestamp': {'timestampValue': datetime.datetime.utcnow().isoformat() + "Z"},
                'uid': {'stringValue': self.current_user_id}
            }
        }
        
        # --- THIS IS THE FIX ---
        headers = {"Authorization": f"Bearer {self.id_token}"}
        
        # Note: `params` is removed, and `headers` is added
        requests.post(url, headers=headers, json=post_data)
        
        self.root.get_screen("workshop_detail").ids.comment_input.text = ""
        self.load_workshop_comments(workshop_name)
        
    def delete_comment(self, workshop_name, comment_id):
        if not self.id_token: return
        
        collection_path = f'artifacts/{APP_ID}/public/data/workshop_comments_{workshop_name.replace(" ", "_")}'
        url = f"https://firestore.googleapis.com/v1/projects/{APP_ID}/databases/(default)/documents/{collection_path}/{comment_id}"
        
        try:
            requests.delete(url, params={'auth': self.id_token})
            self.load_workshop_comments(workshop_name) # Refresh comments after deleting
        except requests.exceptions.RequestException as e:
            self.show_dialog("Error", "Could not delete comment.")

    def create_comment_widget(self, comment_id, username, message, timestamp, parent_box):
        comment_widget = Factory.CommentWidget()
        comment_widget.comment_id = comment_id 
        comment_widget.username = username
        comment_widget.ids.username_label.text = username 
        comment_widget.ids.timestamp_label.text = timestamp.strftime("%d %b %Y, %H:%M") if hasattr(timestamp, 'strftime') else '..'
        comment_widget.ids.message_label.text = message
        profile_icon = random.choice([self.asset_path(f"assets/profiles/p{i}.png") for i in range(1, 9)])
        comment_widget.ids.profile_image.source = profile_icon
        parent_box.add_widget(comment_widget)

    def reply_to_comment(self, username):
        detail_screen = self.root.get_screen("workshop_detail")
        comment_input = detail_screen.ids.comment_input
        comment_input.text = f"@{username} "
        comment_input.focus = True 
        
    # --- Profile Page Functions (Secure) ---
    def confirm_delete_account(self):
        self.dialog = MDDialog(title="Delete Account?", text="This action is permanent and cannot be undone.",
            buttons=[
                MDTextButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                MDRaisedButton(text="DELETE", md_bg_color=self.theme_cls.error_color, on_release=lambda x: self.delete_account_permanently()),
            ],
        )
        self.dialog.open()
    
    def delete_account_permanently(self):
        self.dialog.dismiss()
        if not self.id_token: return

        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:delete?key={FIREBASE_WEB_API_KEY}"
        payload = json.dumps({"idToken": self.id_token})

        try:
            response = requests.post(rest_api_url, data=payload)
            if response.ok:
                doc_url = f"https://firestore.googleapis.com/v1/projects/{APP_ID}/databases/(default)/documents/users/{self.current_user_id}"
                requests.delete(doc_url, params={'auth': self.id_token})
                self.show_dialog("Success", "Your account has been permanently deleted.")
                self.logout()
            else:
                self.show_dialog("Error", "Could not delete account. Please log in again and retry.")
        except requests.exceptions.RequestException:
            self.show_dialog("Error", "A connection error occurred.")

    def show_about_dialog(self):
        self.dialog = MDDialog(title="About Kalaatokri", text=f"Version {self.version}\n\nKalaatokri is a creative space for art enthusiasts.",
            buttons=[MDTextButton(text="CLOSE", on_release=lambda x: self.dialog.dismiss())],
        )
        self.dialog.open()
    
    def send_feedback(self):
        try:
            recipient = "kalaatokri@gmail.com"
            subject = f"Kalaatokri App Feedback (v{self.version})"
            webbrowser.open(f"mailto:{recipient}?subject={subject}")
        except Exception:
            self.show_dialog("Error", "Could not open email client.")

    # --- Utility and Other Functions ---
    def show_dialog(self, title, text):
        self.dialog = MDDialog(title=title, text=text,
            buttons=[MDTextButton(text="OK", on_release=lambda x: self.dialog.dismiss())],
        )
        self.dialog.open()
        
    def go_home(self): self.root.current = "home"
    def open_link(self, url): webbrowser.open(url)
    def show_gallery(self, image, description):
        detail_screen = self.root.get_screen("gallery_detail")
        detail_screen.ids.gallery_image.source = image
        detail_screen.ids.gallery_text.text = description
        self.root.current = "gallery_detail"
    def show_faq_dialog(self):
        """Displays a scrollable dialog with Frequently Asked Questions."""
        
        faq_content = {
            "What makes Kalaatokri's online art workshops unique and why should I consider joining them?": "Kalaatokri's online art workshops stand out due to our unique blend of creativity and therapeutic benefits. Our experienced instructors guide you through various forms of art therapy and craft projects that are designed to unleash your creativity while providing a form of emotional expression and stress relief. Whether you are a beginner or an experienced artist, Kalaatokri offers tailored sessions to meet your individual needs. Additionally, our workshops are conducted online, providing you with the flexibility to learn from the comfort of your home. Joining Kalaatokri means more than just learning art; it's about discovering a new way to relax, enjoy, and express yourself.",
            "Can I change my username?": "Currently, changing your username after registration is not supported. Please choose your username carefully.",
            "Is my data secure?": "We take user privacy seriously. All authentication is handled securely by Firebase, and your data is protected by Firestore's security rules.",
            "How can I provide feedback?": "We'd love to hear from you! You can send us your suggestions by tapping the 'Send Feedback' button on the Profile page.",
            "What happens if I miss a live session for a Kalaatokri online art workshop?":"At Kalaatokri, we understand that life can sometimes get in the way of your creative pursuits. If you miss a live session, don't worry—you won't miss out on the valuable content. All our live sessions are recorded and made available to participants within 24 hours. You will receive an email with a link to access the recorded session, allowing you to catch up at your own pace. Additionally, you can reach out to our support team for any specific questions or clarifications. This way, you can continue your journey towards unleashing your creativity through our art therapy and craft workshops without any interruptions.",
            "If I have doubts or queries in recorded sessions, how can Kalaatokri assist me?":"At Kalaatokri, we understand that questions and doubts can arise even during recorded sessions of our online art therapy and craft workshops. To ensure you have a seamless and supportive learning experience, we offer several ways to assist you:  \n1. Email Support: You can send your queries to our dedicated support team at support@kalatókrri.com. Our team will respond within 24-48 hours with detailed answers to help resolve your doubts.  \n2. Discussion Forums: We provide access to online community forums where you can post your questions. Both our instructors and fellow participants can offer insights and solutions, fostering a collaborative learning environment.  \n3. Live Q&A Sessions: We periodically host live Q&A sessions where you can join and ask any questions you might have from the recorded sessions. These sessions are scheduled regularly, and the dates are communicated well in advance.  \n4. One-on-One Consultations: For more personalized assistance, you can book a one-on-one consultation with our experienced instructors. This option allows for a more in-depth discussion of your specific queries related to the recorded sessions.  Your learning journey is important to us, and we are committed to providing all the necessary support to help you unleash your creativity with Kalaatokri."
        }

        scroll = ScrollView(
            size_hint_y=None,
            height=dp(400)  
        )
        
        list_view = MDList(adaptive_height=True)

        for question, answer in faq_content.items():
            list_view.add_widget(MDLabel(
                text=f"[b]{question}[/b]",
                markup=True,
                theme_text_color="Primary",
                padding=(dp(15), dp(10)),
                adaptive_height=True
            ))
            list_view.add_widget(MDLabel(
                text=answer,
                theme_text_color="Secondary",
                padding=(dp(15), 0, dp(15), dp(15)),
                adaptive_height=True
            ))

        scroll.add_widget(list_view)

        self.dialog = MDDialog(
            title="Frequently Asked Questions",
            type="custom",
            content_cls=scroll,  
            buttons=[
                MDTextButton(
                    text="CLOSE",
                    on_release=lambda x: self.dialog.dismiss(),
                ),
            ],
        )
        self.dialog.open()



if __name__ == "__main__":
    MainApp().run()

