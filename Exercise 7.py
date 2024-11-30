# Exercise 7: Encrypted Chat
import flet as ft
from cryptography.fernet import Fernet
import os

key = Fernet.generate_key()
cipher_suite = Fernet(key)
os.environ["MY_APP_SECRET_KEY"] = key.decode("utf-8")

def main(page: ft.Page):
    page.title = "Encrypted Chat App"
    page.theme_mode = "light"
    secret_key = os.getenv("MY_APP_SECRET_KEY").encode("utf-8")
    cipher_suite = Fernet(secret_key)

    chat_topics = {}

    passphrase = ft.TextField(hint_text="Enter your passphrase", password=True, width=300)
    user = ft.TextField(hint_text="Your name", width=150)
    message = ft.TextField(hint_text="Your message...", expand=True)
    topic_selector = ft.Dropdown(
        label="Select topic",
        options=[
            ft.dropdown.Option("Select topic"),
            ft.dropdown.Option("General"),
            ft.dropdown.Option("Personal"),
            ft.dropdown.Option("Work"),
            ft.dropdown.Option("Social"),
        ],
        value="Select topic",
    )
    messages = ft.Column(scroll="always")
    send_button = ft.ElevatedButton("Send")
    decrypt_button = ft.ElevatedButton("Decrypt Messages")

    def on_message(msg):
        messages.controls.append(ft.Text(msg))
        page.update()

    page.pubsub.subscribe(on_message)

    def send_click(e):
        if not user.value or not message.value or not passphrase.value or topic_selector.value == "Select topic":
            messages.controls.append(ft.Text("⚠️ Please fill out all fields and select a valid topic!"))
            page.update()
            return

        selected_topic = topic_selector.value
        plain_text = f"{user.value}: {message.value}"
        try:
            encrypted_text = cipher_suite.encrypt(plain_text.encode("utf-8")).decode("utf-8")
        except Exception as ex:
            messages.controls.append(ft.Text(f"⚠️ Encryption failed: {ex}"))
            page.update()
            return

        chat_topics.setdefault(selected_topic, []).append(encrypted_text)
        page.pubsub.send_all(f"[{selected_topic}] {encrypted_text}")
        message.value = ""
        page.update()

    def decrypt_click(e):
        if not passphrase.value:
            messages.controls.append(ft.Text("Please enter your passphrase to decrypt messages!"))
            page.update()
            return

        selected_topic = topic_selector.value
        decrypted_msgs = []
        for encrypted_text in chat_topics.get(selected_topic, []):
            try:
                decrypted_text = cipher_suite.decrypt(encrypted_text.encode("utf-8")).decode("utf-8")
                decrypted_msgs.append(decrypted_text)
            except Exception:
                decrypted_msgs.append("Failed to decrypt message.")

        messages.controls.clear()
        for msg in decrypted_msgs:
            messages.controls.append(ft.Text(msg))
        page.update()

    send_button.on_click = send_click
    decrypt_button.on_click = decrypt_click

    page.add(
        ft.Row([ft.Text("Encrypted Chat App", size=24)]),
        ft.Row([user, passphrase]),
        topic_selector,
        ft.Row([message, send_button, decrypt_button]),
        messages,
    )

ft.app(main)
