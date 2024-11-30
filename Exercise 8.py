# Excercise 8: Charts and Tables

import flet as ft

def main(page: ft.Page):
    page.title = "Expense Tracker with PieChart Icons"
    page.theme_mode = "light"
    categories = ["Food", "Travel", "Entertainment", "Miscellaneous"]
    expenses = {"Food": 0, "Travel": 0, "Entertainment": 0, "Miscellaneous": 0}

    previous_descriptions = []  # To store previously entered descriptions

    # PieChart styles
    normal_radius = 100
    normal_title_style = ft.TextStyle(
        size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
    )

    # Badge creation
    def badge(icon, size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.colors.WHITE,
        )

    # Mapping categories to icons and colors
    category_icons = {
        "Food": ft.icons.RESTAURANT,
        "Travel": ft.icons.FLIGHT,
        "Entertainment": ft.icons.MOVIE,
        "Miscellaneous": ft.icons.CATEGORY,
    }
    category_colors = {
        "Food": ft.colors.RED,
        "Travel": ft.colors.BLUE,
        "Entertainment": ft.colors.GREEN,
        "Miscellaneous": ft.colors.YELLOW,
    }

    # Function to create PieChart sections dynamically
    def create_pie_chart_sections():
        total = sum(expenses.values())
        sections = []
        for category, amount in expenses.items():
            percentage = (amount / total) * 100 if total > 0 else 0
            sections.append(
                ft.PieChartSection(
                    value=amount,
                    title=f"{percentage:.1f}%" if total > 0 else "0.0%",
                    title_style=normal_title_style,
                    color=category_colors.get(category, ft.colors.GREY),
                    radius=normal_radius,
                    badge=badge(category_icons.get(category, ft.icons.CATEGORY), 40),
                    badge_position=0.98,
                )
            )
        return sections

    # PieChart instance
    pie_chart = ft.PieChart(
        sections=create_pie_chart_sections(),
        sections_space=0,
        center_space_radius=40,
        expand=True,
    )

    # Function to update PieChart
    def update_pie_chart():
        pie_chart.sections = create_pie_chart_sections()
        pie_chart.update()

    # Input fields for adding expenses
    category_input = ft.Dropdown(
        label="Category",
        options=[ft.dropdown.Option(category) for category in categories],
    )

    # Dropdown for description autocomplete
    description_input = ft.TextField(label="Description")
    description_autocomplete = ft.Dropdown(
        label="Previous Descriptions",
        options=[],
        visible=False,
    )

    def show_autocomplete(e):
        query = description_input.value.lower()
        matches = [desc for desc in previous_descriptions if query in desc.lower()]
        if matches:
            description_autocomplete.options = [ft.dropdown.Option(desc) for desc in matches]
            description_autocomplete.visible = True
        else:
            description_autocomplete.visible = False
        description_autocomplete.update()

    description_input.on_change = show_autocomplete

    def select_autocomplete(e):
        description_input.value = description_autocomplete.value
        description_autocomplete.visible = False
        description_input.update()
        description_autocomplete.update()

    description_autocomplete.on_change = select_autocomplete

    amount_input = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER)

    # DataTable for expense list
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Category")),
            ft.DataColumn(ft.Text("Description")),
            ft.DataColumn(ft.Text("Amount"), numeric=True),
        ],
        rows=[],
        expand=True,
    )

    # Function to handle adding an expense
    def add_expense(e):
        category = category_input.value
        description = description_input.value
        try:
            amount = float(amount_input.value)
        except ValueError:
            amount_input.error_text = "Please enter a valid number"
            amount_input.update()
            return

        if not category or not description or amount <= 0:
            return

        # Update expenses
        expenses[category] += amount

        # Add description to autocomplete suggestions
        if description not in previous_descriptions:
            previous_descriptions.append(description)

        # Add entry to DataTable
        data_table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(category)),
                    ft.DataCell(ft.Text(description)),
                    ft.DataCell(ft.Text(f"{amount:.2f}")),
                ]
            )
        )
        data_table.update()

        # Update PieChart
        update_pie_chart()

        # Clear input fields
        category_input.value = None
        description_input.value = ""
        amount_input.value = ""
        description_autocomplete.visible = False
        category_input.update()
        description_input.update()
        amount_input.update()
        description_autocomplete.update()

    # Add button
    add_button = ft.ElevatedButton("Add Expense", on_click=add_expense)

    # Page layout
    page.add(
        ft.Column(
            [
                ft.Text("Expense Tracker with Icons", size=24, weight=ft.FontWeight.BOLD),
                ft.Row([category_input, description_input, description_autocomplete]),
                ft.Row([amount_input, add_button]),
                ft.Row(
                    [
                        ft.Container(data_table, expand=1, padding=ft.padding.all(10)),
                        ft.Container(pie_chart, expand=1, padding=ft.padding.all(10)),
                    ],
                    spacing=20,
                    expand=True,
                ),
            ],
            spacing=20,
            expand=True,
        )
    )

ft.app(target=main)
