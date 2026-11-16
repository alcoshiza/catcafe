import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from engine import GameEngine
from interfaces import IEvent

class ModernCatCafeGUI(tk.Tk):
    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self.current_event: Optional[IEvent] = None

        self.title("🐾 Симулятор Котячого Кафе 🐾")
        self.geometry("1140x780")
        self.minsize(1060, 720)
        self.configure(bg="#1E1B1A")

        self._setup_styles()
        self._create_widgets()
        self._update_status_display()
        self._show_welcome_state()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Колірна палітра "Warm Espresso, Cream & Terracotta"
        self.bg_dark = "#1E1B1A"
        self.card_bg = "#2B2423"
        self.card_accent = "#38302D"
        self.text_primary = "#F5EBE6"
        self.text_secondary = "#BCAEAA"
        self.accent_color = "#C87D55"
        self.accent_hover = "#DF8F63"
        self.success_color = "#4EAA78"
        self.danger_color = "#D95D5D"
        self.warning_color = "#E5A84B"

        self.style.configure("TFrame", background=self.bg_dark)
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        self.style.configure("CardInner.TFrame", background=self.card_accent, relief="flat")

        # Заголовки та написи
        self.style.configure("Header.TLabel", background=self.bg_dark, foreground=self.text_primary, font=("Segoe UI", 16, "bold"))
        self.style.configure("DayBadge.TLabel", background="#C87D55", foreground="#FFFFFF", font=("Segoe UI", 11, "bold"), padding=(12, 4))
        self.style.configure("StatusTitle.TLabel", background=self.card_bg, foreground=self.text_secondary, font=("Segoe UI", 9))
        self.style.configure("StatusVal.TLabel", background=self.card_bg, foreground=self.text_primary, font=("Segoe UI", 13, "bold"))
        self.style.configure("CardHeader.TLabel", background=self.card_bg, foreground=self.text_primary, font=("Segoe UI", 12, "bold"))
        self.style.configure("SubText.TLabel", background=self.card_bg, foreground=self.text_secondary, font=("Segoe UI", 9))
        self.style.configure("EventTitle.TLabel", background=self.card_bg, foreground="#FFB347", font=("Segoe UI", 11, "bold"))
        self.style.configure("EventDesc.TLabel", background=self.card_bg, foreground=self.text_primary, font=("Segoe UI", 10))

        # Кнопки
        self.style.configure("Accent.TButton", background=self.accent_color, foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), borderwidth=0, padding=8)
        self.style.map("Accent.TButton", background=[("active", self.accent_hover), ("disabled", "#554A46")])

        self.style.configure("Secondary.TButton", background=self.card_accent, foreground=self.text_primary, font=("Segoe UI", 9, "bold"), borderwidth=0, padding=6)
        self.style.map("Secondary.TButton", background=[("active", "#4A403C")])

        self.style.configure("Event.TButton", background="#3E3432", foreground="#FFFFFF", font=("Segoe UI", 9), borderwidth=0, padding=(10, 8), wraplength=330, justify="left")
        self.style.map("Event.TButton", background=[("active", "#524643")])

        # Вкладки (Notebook)
        self.style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.card_bg, foreground=self.text_secondary, font=("Segoe UI", 10, "bold"), padding=(16, 8), borderwidth=0)
        self.style.map("TNotebook.Tab",
            background=[("selected", self.accent_color), ("active", self.card_accent)],
            foreground=[("selected", "#FFFFFF"), ("active", self.text_primary)]
        )

        # Таблиця історії (Treeview)
        self.style.configure("Treeview",
            background=self.card_bg,
            foreground=self.text_primary,
            fieldbackground=self.card_bg,
            rowheight=28,
            font=("Segoe UI", 9)
        )
        self.style.configure("Treeview.Heading",
            background=self.card_accent,
            foreground=self.text_primary,
            font=("Segoe UI", 9, "bold"),
            borderwidth=0
        )
        self.style.map("Treeview", background=[("selected", self.accent_color)])

    def _create_widgets(self):
        # 1. Верхня панель (Заголовок, налаштування тривалості гри, статус дня)
        top_bar = ttk.Frame(self, style="TFrame")
        top_bar.pack(fill="x", padx=20, pady=(15, 10))

        # Ліва частина топ-бару: Назва кафе
        title_box = ttk.Frame(top_bar, style="TFrame")
        title_box.pack(side="left")
        ttk.Label(title_box, text="🐾 Cat Café Manager", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_box, text="Затишне кафе з пухнастими улюбленцями", style="SubText.TLabel", background=self.bg_dark).pack(anchor="w")

        # Права частина топ-бару: Масштабування тривалості гри + Бейдж дня
        controls_box = ttk.Frame(top_bar, style="TFrame")
        controls_box.pack(side="right")

        ttk.Label(controls_box, text="📅 Тривалість:", style="SubText.TLabel", background=self.bg_dark).pack(side="left", padx=(0, 6))

        self.spin_days = ttk.Spinbox(controls_box, from_=1, to=100, width=4, font=("Segoe UI", 10, "bold"), justify="center")
        self.spin_days.set(str(self.engine.state.max_days))
        self.spin_days.pack(side="left", padx=(0, 10))
        self.spin_days.bind("<FocusOut>", self._on_duration_changed)
        self.spin_days.bind("<Return>", self._on_duration_changed)

        btn_apply_days = ttk.Button(controls_box, text="Застосувати", style="Secondary.TButton", command=self._on_duration_changed)
        btn_apply_days.pack(side="left", padx=(0, 10))

        btn_new_game = ttk.Button(controls_box, text="🔄 Нова гра", style="Secondary.TButton", command=self._on_restart_game)
        btn_new_game.pack(side="left", padx=(0, 15))

        self.lbl_day_badge = ttk.Label(controls_box, text="ДЕНЬ 1 / 5", style="DayBadge.TLabel")
        self.lbl_day_badge.pack(side="left")

        # 2. Метрики / KPI картки (Бюджет, Зерна, Репутація)
        metrics_bar = ttk.Frame(self, style="TFrame")
        metrics_bar.pack(fill="x", padx=20, pady=5)
        metrics_bar.columnconfigure((0, 1, 2), weight=1, uniform="metric")

        # Картка 1: Бюджет
        card_budget = ttk.Frame(metrics_bar, style="Card.TFrame", padding=12)
        card_budget.grid(row=0, column=0, padx=(0, 6), sticky="nsew")
        ttk.Label(card_budget, text="💰 БЮДЖЕТ КАФЕ", style="StatusTitle.TLabel").pack(anchor="w")
        self.lbl_budget_val = ttk.Label(card_budget, text="2500.00 грн", style="StatusVal.TLabel")
        self.lbl_budget_val.pack(anchor="w", pady=(3, 0))

        # Картка 2: Запаси кави
        card_beans = ttk.Frame(metrics_bar, style="Card.TFrame", padding=12)
        card_beans.grid(row=0, column=1, padx=6, sticky="nsew")
        ttk.Label(card_beans, text="☕ ЗАПАСИ ЗЕРЕН", style="StatusTitle.TLabel").pack(anchor="w")
        self.lbl_beans_val = ttk.Label(card_beans, text="20 порцій", style="StatusVal.TLabel")
        self.lbl_beans_val.pack(anchor="w", pady=(3, 0))

        # Картка 3: Репутація
        card_rep = ttk.Frame(metrics_bar, style="Card.TFrame", padding=12)
        card_rep.grid(row=0, column=2, padx=(6, 0), sticky="nsew")
        ttk.Label(card_rep, text="⭐ РЕПУТАЦІЯ ЗАКЛАДУ", style="StatusTitle.TLabel").pack(anchor="w")
        self.lbl_rep_val = ttk.Label(card_rep, text="70.0 / 100", style="StatusVal.TLabel")
        self.lbl_rep_val.pack(anchor="w", pady=(3, 0))

        # 3. Основний робочий простір (Ліва панель керування + Права інтерактивна зала)
        workspace = ttk.Frame(self, style="TFrame")
        workspace.pack(fill="both", expand=True, padx=20, pady=(10, 15))

        # ================= ЛІВА КОЛОНКА (Управління зміною) =================
        left_col = ttk.Frame(workspace, style="Card.TFrame", padding=16, width=390)
        left_col.pack(side="left", fill="y", padx=(0, 10))
        left_col.pack_propagate(False)

        ttk.Label(left_col, text="⚙️ Керування зміною", style="CardHeader.TLabel").pack(anchor="w", pady=(0, 12))

        # Блок закупівлі
        ttk.Label(left_col, text="🛒 Закупівля кави (25 грн / порція):", style="SubText.TLabel").pack(anchor="w", pady=(0, 4))
        self.ent_beans = ttk.Entry(left_col, font=("Segoe UI", 10))
        self.ent_beans.insert(0, "5")
        self.ent_beans.pack(fill="x", pady=(0, 10))

        # Блок ціни кави
        ttk.Label(left_col, text="🏷️ Ціна чашки на день (грн):", style="SubText.TLabel").pack(anchor="w", pady=(0, 4))
        self.ent_price = ttk.Entry(left_col, font=("Segoe UI", 10))
        self.ent_price.insert(0, "60")
        self.ent_price.pack(fill="x", pady=(0, 15))

        # Головна кнопка запуску зміни
        self.btn_start_day = ttk.Button(left_col, text="▶️ Розпочати зміну", style="Accent.TButton", command=self._on_start_day)
        self.btn_start_day.pack(fill="x", ipady=6, pady=(0, 12))

        # Картка події (форс-мажору)
        self.event_card = ttk.Frame(left_col, style="CardInner.TFrame", padding=12)
        self.lbl_event_title = ttk.Label(self.event_card, text="", style="EventTitle.TLabel", background=self.card_accent, wraplength=340, justify="left")
        self.lbl_event_title.pack(anchor="w", pady=(0, 5))

        self.lbl_event_desc = ttk.Label(self.event_card, text="", style="EventDesc.TLabel", wraplength=340, justify="left", background=self.card_accent)
        self.lbl_event_desc.pack(anchor="w", pady=(0, 10))

        self.event_options_container = ttk.Frame(self.event_card, style="CardInner.TFrame")
        self.event_options_container.pack(fill="x")

        # ================= ПРАВА КОЛОНКА (Сучасний інтерактивний інтерфейс) =================
        right_col = ttk.Frame(workspace, style="TFrame")
        right_col.pack(side="right", fill="both", expand=True)

        self.notebook = ttk.Notebook(right_col)
        self.notebook.pack(fill="both", expand=True)

        # Вкладка 1: Зала кафе та відвідувачі
        self.tab_hall = ttk.Frame(self.notebook, style="Card.TFrame", padding=14)
        self.notebook.add(self.tab_hall, text="☕ Зала кафе та замовлення")

        # Вкладка 2: Наші котики
        self.tab_cats = ttk.Frame(self.notebook, style="Card.TFrame", padding=14)
        self.notebook.add(self.tab_cats, text="🐾 Наші котики")

        # Вкладка 3: Історія змін
        self.tab_history = ttk.Frame(self.notebook, style="Card.TFrame", padding=14)
        self.notebook.add(self.tab_history, text="📈 Фінанси та історія")

        self._build_hall_tab()
        self._build_cats_tab()
        self._build_history_tab()

    def _build_hall_tab(self):
        # Банер стану зміни
        self.shift_banner = ttk.Frame(self.tab_hall, style="CardInner.TFrame", padding=12)
        self.shift_banner.pack(fill="x", pady=(0, 12))

        self.lbl_shift_title = ttk.Label(self.shift_banner, text="☀️ Зміна готова до відкриття", font=("Segoe UI", 11, "bold"), background=self.card_accent, foreground=self.text_primary)
        self.lbl_shift_title.pack(anchor="w")

        self.lbl_shift_stats = ttk.Label(self.shift_banner, text="Оберіть закупівлю зерен та встановіть ціну напою ліворуч, потім натисніть 'Розпочати зміну'.", font=("Segoe UI", 9), background=self.card_accent, foreground=self.text_secondary)
        self.lbl_shift_stats.pack(anchor="w", pady=(4, 0))

        # Заголовок списку гостей
        list_header = ttk.Frame(self.tab_hall, style="Card.TFrame")
        list_header.pack(fill="x", pady=(0, 8))
        ttk.Label(list_header, text="👥 Відвідувачі сьогоднішньої зміни", font=("Segoe UI", 11, "bold"), style="CardHeader.TLabel").pack(side="left")
        self.lbl_guest_count_badge = ttk.Label(list_header, text="0 гостей", font=("Segoe UI", 9, "bold"), background=self.card_accent, foreground=self.text_secondary, padding=(8, 2))
        self.lbl_guest_count_badge.pack(side="right")

        # Скрольований контейнер для карток клієнтів
        container = ttk.Frame(self.tab_hall, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        self.canvas_customers = tk.Canvas(container, bg=self.card_bg, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas_customers.yview)

        self.customers_frame = ttk.Frame(self.canvas_customers, style="Card.TFrame")
        self.customers_frame.bind(
            "<Configure>",
            lambda e: self.canvas_customers.configure(scrollregion=self.canvas_customers.bbox("all"))
        )

        self.canvas_window = self.canvas_customers.create_window((0, 0), window=self.customers_frame, anchor="nw")
        self.canvas_customers.bind(
            "<Configure>",
            lambda e: self.canvas_customers.itemconfig(self.canvas_window, width=e.width)
        )

        self.canvas_customers.configure(yscrollcommand=scrollbar.set)
        self.canvas_customers.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Додаємо підтримку скролу колесом миші
        def _on_mousewheel(event):
            self.canvas_customers.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas_customers.bind_all("<MouseWheel>", _on_mousewheel)

    def _build_cats_tab(self):
        ttk.Label(self.tab_cats, text="🐈 Пухнасті мешканці кафе", font=("Segoe UI", 12, "bold"), style="CardHeader.TLabel").pack(anchor="w", pady=(0, 4))
        ttk.Label(self.tab_cats, text="Котики створюють затишну атмосферу та підвищують настрій відвідувачів!", style="SubText.TLabel").pack(anchor="w", pady=(0, 10))

        # Скрольований контейнер для всіх котиків
        container = ttk.Frame(self.tab_cats, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        canvas_cats = tk.Canvas(container, bg=self.card_bg, highlightthickness=0, borderwidth=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas_cats.yview)

        cats_inner_frame = ttk.Frame(canvas_cats, style="Card.TFrame")
        cats_inner_frame.bind(
            "<Configure>",
            lambda e: canvas_cats.configure(scrollregion=canvas_cats.bbox("all"))
        )

        canvas_window = canvas_cats.create_window((0, 0), window=cats_inner_frame, anchor="nw")
        canvas_cats.bind(
            "<Configure>",
            lambda e: canvas_cats.itemconfig(canvas_window, width=e.width)
        )

        canvas_cats.configure(yscrollcommand=scrollbar.set)
        canvas_cats.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        cats_grid = ttk.Frame(cats_inner_frame, style="Card.TFrame")
        cats_grid.pack(fill="both", expand=True)
        cats_grid.columnconfigure((0, 1), weight=1, uniform="cat")

        for idx, cat in enumerate(self.engine.resident_cats):
            row = idx // 2
            col = idx % 2

            cat_card = ttk.Frame(cats_grid, style="CardInner.TFrame", padding=12)
            cat_card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            top_row = ttk.Frame(cat_card, style="CardInner.TFrame")
            top_row.pack(fill="x")

            ttk.Label(top_row, text=cat["icon"], font=("Segoe UI Emoji", 22), background=self.card_accent).pack(side="left", padx=(0, 10))

            info_box = ttk.Frame(top_row, style="CardInner.TFrame")
            info_box.pack(side="left", fill="x", expand=True)

            ttk.Label(info_box, text=cat["name"], font=("Segoe UI", 11, "bold"), foreground=self.text_primary, background=self.card_accent).pack(anchor="w")
            ttk.Label(info_box, text=f"Порода: {cat['breed']}", font=("Segoe UI", 9), foreground=self.text_secondary, background=self.card_accent).pack(anchor="w")

            mood_lbl = ttk.Label(cat_card, text=f"Настрій: {cat['mood']}", font=("Segoe UI", 9, "italic"), foreground="#FFB347", background=self.card_accent)
            mood_lbl.pack(anchor="w", pady=(8, 6))

            btn_pet = ttk.Button(cat_card, text="Погладити котика ❤️", style="Secondary.TButton",
                                 command=lambda c=cat["name"]: self._on_pet_cat(c))
            btn_pet.pack(fill="x")

    def _on_pet_cat(self, cat_name: str):
        reactions = {
            "Барсік": "Барсік солодко позіхнув, витягнув пухнасте пузико та знову заснув 💤",
            "Скумбрія": "Скумбрія потерлася об ногу і тихо замуркотіла: 'А де рибка? Хоч кусочок!' 🐟",
            "Прікол": "Прікол зробив потрійне сальто, вкусив за шнурок і побіг за уявним метеликом ⚡",
            "Люся": "Люся дозволила торкнутися своєї королівської шерсті й з гідністю замуркотіла 👑",
            "Тузік": "Тузік віддав честь хвостом і гордо загарчав у бік вхідних дверей 🐕",
            "Шарік": "Шарік перекотився на спинку як пухнастий колобок і підставив животик ❤️",
            "Кульок": "Кульок радісно заліз у найближчий паперовий пакет і голосно зашелестів 🛍️"
        }
        text = reactions.get(cat_name, f"Кіт {cat_name} задоволено муркоче!")
        messagebox.showinfo(f"Муррр! 🐾 ({cat_name})", text)

    def _build_history_tab(self):
        ttk.Label(self.tab_history, text="📊 Звітність по змінах", font=("Segoe UI", 12, "bold"), style="CardHeader.TLabel").pack(anchor="w", pady=(0, 12))

        columns = ("day", "guests", "served", "unserved", "revenue", "rep")
        self.tree_history = ttk.Treeview(self.tab_history, columns=columns, show="headings", height=12)

        self.tree_history.heading("day", text="День")
        self.tree_history.heading("guests", text="Всього гостей")
        self.tree_history.heading("served", text="Обслуговано")
        self.tree_history.heading("unserved", text="Не вистачило зерен")
        self.tree_history.heading("revenue", text="Виручка (грн)")
        self.tree_history.heading("rep", text="Зміна репутації")

        self.tree_history.column("day", width=70, anchor="center")
        self.tree_history.column("guests", width=110, anchor="center")
        self.tree_history.column("served", width=110, anchor="center")
        self.tree_history.column("unserved", width=140, anchor="center")
        self.tree_history.column("revenue", width=120, anchor="center")
        self.tree_history.column("rep", width=120, anchor="center")

        self.tree_history.pack(fill="both", expand=True)

    def _on_pet_cat(self, cat_name: str):
        messagebox.showinfo("Муррр! 🐾", f"Кіт {cat_name} задоволено замружив очі та потерся об вашу руку! (+1 гарний настрій)")

    def _on_duration_changed(self, event=None):
        try:
            val = int(self.spin_days.get())
            if val < 1:
                raise ValueError
            self.engine.set_max_days(val)
            self._update_status_display()
        except ValueError:
            messagebox.showerror("Помилка", "Будь ласка, вкажіть коректне число днів (щонайменше 1).")
            self.spin_days.set(str(self.engine.state.max_days))

    def _on_restart_game(self):
        confirm = messagebox.askyesno("Нова гра", "Ви впевнені, що бажаєте скинути прогрес та розпочати нову зміну?")
        if confirm:
            try:
                days = int(self.spin_days.get())
            except ValueError:
                days = 5
            self.engine.init_game(max_days=days)
            self.event_card.pack_forget()
            self.btn_start_day.config(state="normal")
            self._update_status_display()
            self._show_welcome_state()
            # Очищуємо історію в таблиці
            for row in self.tree_history.get_children():
                self.tree_history.delete(row)

    def _show_welcome_state(self):
        # Очищуємо картки клієнтів
        for child in self.customers_frame.winfo_children():
            child.destroy()

        welcome_card = ttk.Frame(self.customers_frame, style="CardInner.TFrame", padding=20)
        welcome_card.pack(fill="x", padx=4, pady=8)

        ttk.Label(welcome_card, text="☕ Зала відкрита для гостей!", font=("Segoe UI", 12, "bold"), foreground=self.text_primary, background=self.card_accent).pack(anchor="w")
        ttk.Label(welcome_card, text="Закупте зерна кави та встановіть ціну чашки в панелі ліворуч, після чого натисніть 'Розпочати зміну'.\nКожен гість матиме своє візуальне замовлення та статус обслуговування.",
                  font=("Segoe UI", 9), foreground=self.text_secondary, background=self.card_accent, wraplength=550).pack(anchor="w", pady=(6, 0))

        self.lbl_guest_count_badge.config(text="0 гостей")
        self.lbl_shift_title.config(text="☀️ Зміна готова до відкриття")
        self.lbl_shift_stats.config(text="Очікується запуск нового робочого дня.")

    def _update_status_display(self):
        st = self.engine.state
        self.lbl_day_badge.config(text=f"ДЕНЬ {st.current_day} / {st.max_days}")
        self.lbl_budget_val.config(text=f"{st.budget.value:.2f} грн")
        self.lbl_beans_val.config(text=f"{st.beans.count} порцій")
        self.lbl_rep_val.config(text=f"{st.reputation.value} / 100")

    def _on_start_day(self):
        try:
            beans_to_buy = int(self.ent_beans.get())
            cup_price = float(self.ent_price.get())
            if cup_price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка введення", "Будь ласка, введіть коректні числові значення для кількості зерен та ціни!")
            return

        # 1. Закупівля
        success, msg = self.engine.buy_supplies(beans_to_buy)
        self._update_status_display()
        if not success:
            messagebox.showwarning("Недостатньо коштів", msg)
            return

        # 2. Випадкова подія ранку
        self.current_event = self.engine.get_random_event()
        self._show_event_ui(self.current_event, cup_price)

    def _show_event_ui(self, event: IEvent, cup_price: float):
        self.btn_start_day.config(state="disabled")
        self.event_card.pack(fill="x", pady=(10, 0))
        self.lbl_event_title.config(text=event.title)
        self.lbl_event_desc.config(text=event.description)

        for child in self.event_options_container.winfo_children():
            child.destroy()

        for idx, option_text in enumerate(event.options):
            btn = ttk.Button(
                self.event_options_container,
                text=option_text,
                style="Event.TButton",
                command=lambda i=idx: self._handle_event_choice(i, cup_price)
            )
            btn.pack(fill="x", pady=2)

    def _handle_event_choice(self, choice_idx: int, cup_price: float):
        res = self.engine.process_event_choice(self.current_event, choice_idx)
        self.event_card.pack_forget()
        self._update_status_display()

        if self.engine.state.is_bankrupt:
            self._game_over(False)
            return

        # 3. Симуляція обслуговування дня
        self.engine.simulate_day(cup_price)
        self._update_status_display()

        # Відображення результатів зміни у красивому графічному вигляді
        self._render_shift_results(res)

        if self.engine.state.is_bankrupt:
            self._game_over(False)
            return

        # Перевірка на завершення гри
        if self.engine.state.current_day >= self.engine.state.max_days:
            self._game_over(True)
        else:
            self.engine.next_day()
            self._update_status_display()
            self.btn_start_day.config(state="normal")

    def _render_shift_results(self, event_result: str):
        stats = self.engine.last_shift_stats
        customers = self.engine.last_shift_customers

        # Оновлення банера зміни
        self.lbl_shift_title.config(
            text=f"✨ Підсумки зміни Дня {stats['day']}: Виручка +{stats['revenue']:.2f} грн"
        )
        self.lbl_shift_stats.config(
            text=f"Обслуговано: {stats['served']} з {stats['total_guests']} гостей | Подія ранку: {event_result}"
        )
        self.lbl_guest_count_badge.config(text=f"{stats['total_guests']} гостей")

        # Очищення старих карток
        for child in self.customers_frame.winfo_children():
            child.destroy()

        # Створення сучасних карток клієнтів
        for cust in customers:
            card = ttk.Frame(self.customers_frame, style="CardInner.TFrame", padding=10)
            card.pack(fill="x", padx=4, pady=4)

            # Аватар та ім'я
            left_info = ttk.Frame(card, style="CardInner.TFrame")
            left_info.pack(side="left", fill="x", expand=True)

            avatar_text = "👤" if cust["served"] else "🚶"
            header_line = ttk.Frame(left_info, style="CardInner.TFrame")
            header_line.pack(anchor="w")

            ttk.Label(header_line, text=avatar_text, font=("Segoe UI Emoji", 14), background=self.card_accent).pack(side="left", padx=(0, 6))
            ttk.Label(header_line, text=cust["name"], font=("Segoe UI", 11, "bold"), foreground=self.text_primary, background=self.card_accent).pack(side="left")

            order_desc = f"Замовлення: ☕ {cust['drink']}"
            ttk.Label(left_info, text=order_desc, font=("Segoe UI", 9), foreground=self.text_secondary, background=self.card_accent).pack(anchor="w", pady=(2, 0))

            # Статус бейдж
            status_badge = ttk.Frame(card, style="CardInner.TFrame")
            status_badge.pack(side="right")

            if cust["served"]:
                badge_lbl = tk.Label(
                    status_badge,
                    text=f"✓ Виконано (+{cust['price']:.2f} грн)",
                    font=("Segoe UI", 9, "bold"),
                    bg="#244431",
                    fg="#69D193",
                    padx=10,
                    pady=4
                )
            else:
                badge_lbl = tk.Label(
                    status_badge,
                    text="✕ Не вистачило зерен (-4 ⭐)",
                    font=("Segoe UI", 9, "bold"),
                    bg="#4D2020",
                    fg="#FF7A7A",
                    padx=10,
                    pady=4
                )
            badge_lbl.pack()

        # Додавання рядка в історію таблиці
        self.tree_history.insert("", "end", values=(
            f"День {stats['day']}",
            stats["total_guests"],
            stats["served"],
            stats["unserved"],
            f"{stats['revenue']:.2f}",
            f"{stats['rep_delta']:+.1f}"
        ))

    def _game_over(self, victory: bool):
        self.btn_start_day.config(state="disabled")
        self.engine.save_final_report()
        if victory:
            messagebox.showinfo("Перемога! 🎉", f"Вітаємо! Усі дні гри успішно завершено!\nФінальний бюджет кафе: {self.engine.state.budget.value:.2f} грн\nРепутація: {self.engine.state.reputation.value}/100")
        else:
            messagebox.showerror("Банкрутство 💀", "Гроші закінчилися! Кафе зачиняється.")
