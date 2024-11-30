# Exercise 2 PART I

"""
# Hello World App

import flet as ft

def main(page: ft.Page):
    page.title = "Hello World"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    t = ft.Text(value="Hello World", color="black", size=25)
    page.add(t)

ft.app(target=main)



"""
# Modify the code to "Hello IoT", color to "blue", and size to 35.

import flet as ft

def main(page: ft.Page):
    page.title = "Hello IOT"
    page.theme_mode = "light"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    t = ft.Text(value="Hello IoT", color="blue", size=35)
    page.add(t)

ft.app(target=main)

