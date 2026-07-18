import tkinter as tk
from tkinter import ttk, PhotoImage, messagebox, filedialog, simpledialog
import os
import json
from datetime import datetime
import math

# --- KONFIGURASI ---
BG_COLOR, FRAME_COLOR, FONT_COLOR, ACCENT_COLOR = "#F5F5DC", "#FFFFFF", "#3A3B3C", "#D2B48C"
FONT_FAMILY = "Helvetica"
HISTORY_FILE, MENU_DATA_FILE, CONFIG_FILE, CUSTOMERS_FILE = "history.json", "menu_data.json", "config.json", "customers.json"
POIN_PER_RP, NILAI_POIN_RP = 10000, 100
VALID_PROMOS = {"HEMAT10": {"type": "percent", "value": 10}, "NGOPIASIK": {"type": "fixed", "value": 5000}, "ALGOPRO123": {"type": "percent", "value": 15}}
ADMIN_PASSWORD = "admin123" # Password untuk fitur admin

initial_data_products = [
    {"id": 1, "name": "Es Kopi Susu Gula Aren", "price": 22000, "category": "Minuman", "desc": "Kopi susu signature kami yang memadukan espresso kaya rasa dengan susu segar dan manisnya gula aren asli dari Jawa Barat.\n\nKomposisi:\n- House Blend Espresso (70% Arabika Gayo, 30% Robusta)\n- Susu Segar Diamond\n- Gula Aren Organik", "image": "kopi_susu.png", "stock": 20},
    {"id": 2, "name": "Matcha Latte", "price": 28000, "category": "Minuman", "desc": "Berasal dari tradisi upacara minum teh di Jepang, matcha diadopsi oleh kafe global sebagai alternatif kopi yang menenangkan.\n\nAsal: Uji, Kyoto, Jepang.\nBahan Utama:\n- Bubuk Matcha Uji Premium\n- Susu Segar Steam", "image": "matcha_latte.png", "stock": 15},
    {"id": 3, "name": "Strawberry Yogurt", "price": 25000, "category": "Minuman", "desc": "Terinspirasi dari gerakan makanan sehat di California, smoothie ini adalah cara lezat untuk menikmati kebaikan alam.\n\nKomposisi:\n- Buah Stroberi Segar dari perkebunan Lembang\n- Yogurt Plain Creamy\n- Madu Murni", "image": "strawberry_yogurt.png", "stock": 15},
    {"id": 4, "name": "Lychee Tea", "price": 20000, "category": "Minuman", "desc": "Inovasi dari budaya teh modern di Asia Timur. Diciptakan untuk memberikan pilihan yang sangat menyegarkan di cuaca panas.\n\nIsi:\n- Seduhan Teh Hitam Premium\n- Sirup Leci Manis\n- Buah Leci Utuh", "image": "lychee_tea.png", "stock": 30},
    {"id": 5, "name": "Red Velvet Latte", "price": 28000, "category": "Minuman", "desc": "Terinspirasi dari Red Velvet Cake ikonik dari Amerika. Minuman ini adalah 'kue dalam cangkir' (non-kopi).\n\nCatatan Rasa: Cokelat ringan, vanilla, dan sentuhan gurih cream cheese.", "image": "red_velvet.png", "stock": 15},
    {"id": 6, "name": "Cromboloni Cokelat", "price": 30000, "category": "Makanan", "desc": "Sensasi viral dari New York. Perkawinan sempurna antara croissant Prancis dan bomboloni Italia.\n\nKomposisi Utama:\n- Adonan Pastry Mentega\n- Isian Cokelat Belgia Callebaut", "image": "cromboloni.png", "stock": 10},
    {"id": 7, "name": "Korean Garlic Cheese Bread", "price": 35000, "category": "Makanan", "desc": "Berawal dari sebuah toko roti di Gangneung, Korea Selatan, jajanan ini menjadi fenomena street food global.\n\nKomposisi:\n- Roti bun lembut\n- Saus mentega bawang putih melimpah\n- Isian Keju Krim", "image": "korean_garlic.png", "stock": 12},
    {"id": 8, "name": "Spaghetti Brulee", "price": 45000, "category": "Makanan", "desc": "Kreasi modern yang terinspirasi dari Crème brûlée. Konsep 'membakar' lapisan atas diterapkan pada pasta.\n\nKomposisi: Spaghetti Bolognese, Saus Bechamel Creamy, Keju Mozzarella.", "image": "spaghetti_brulee.png", "stock": 10},
    {"id": 9, "name": "Butter Croissant", "price": 20000, "category": "Makanan", "desc": "Mahakarya pastry dari Wina, Austria, yang disempurnakan di Prancis. Kuncinya pada teknik laminasi adonan dan mentega.\n\nCatatan: Sempurna dinikmati langsung atau sebagai pendamping kopi.", "image": "croissant.png", "stock": 25},
    {"id": 10, "name": "Chicken Mentai Rice", "price": 40000, "category": "Makanan", "desc": "Popularitas saus mentai di Jepang diadaptasi menjadi menu 'rice bowl' yang praktis dan mengenyangkan.\n\nSaus Mentai: Mayones Jepang, Tobiko (Telur Ikan Terbang), Bumbu Rahasia.", "image": "mentai_rice.png", "stock": 15},
    {"id": 11, "name": "Biscoff Caramel Latte", "price": 32000, "category": "Minuman", "desc": "Lahir dari tren global biskuit Lotus Biscoff asal Belgia.\n\nCatatan Rasa: Kopi lembut, karamel, kayu manis, dan jahe.", "image": "biscoff_latte.png", "stock": 15},
    {"id": 12, "name": "Ocean Blue Mojito", "price": 27000, "category": "Minuman", "desc": "Adaptasi non-alkohol dari cocktail Mojito klasik asal Kuba. Warna birunya terinspirasi dari keindahan laut Karibia.\n\nKomposisi:\n- Sirup Blue Curacao, Daun Mint, Jeruk Nipis, Air Soda", "image": "ocean_mojito.png", "stock": 20},
    {"id": 13, "name": "Truffle Carbonara", "price": 55000, "category": "Makanan", "desc": "Sentuhan kemewahan pada hidangan carbonara klasik dari Roma, Italia. Penambahan minyak truffle mengangkat hidangan ini menjadi istimewa.\n\nKomposisi Saus: Kuning Telur, Keju Pecorino, Lada Hitam, Minyak Truffle.", "image": "truffle_carbonara.png", "stock": 8},
    {"id": 14, "name": "Dessert Box 'Oreo Puff'", "price": 38000, "category": "Makanan", "desc": "Tren dessert modern yang lahir dari kebutuhan akan kue yang praktis dan 'Instagrammable'.\n\nLapisan: Bolu cokelat, mousse cream cheese, taburan Oreo.", "image": "dessert_box.png", "stock": 10},
    {"id": 15, "name": "Almond Croissant", "price": 28000, "category": "Makanan", "desc": "Secara tradisional, ini adalah cara pembuat roti di Prancis untuk 'menjual kembali' croissant kemarin. Croissant dibelah, diisi pasta almond, dan dipanggang kembali.\n\nKomposisi: Croissant, Isian Frangipane (pasta almond), Taburan Almond.", "image": "almond_croissant.png", "stock": 18},
]

class CafeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("☕ Kafe Kekinian - Sistem Kasir"); self.configure(bg=BG_COLOR); self.attributes('-fullscreen', True); self.bind('<Escape>', self.exit_fullscreen)
        self.cart = {}; self.image_cache = {}; self.transaction_history = []; self.applied_promo = None; self.points_redeemed = 0
        self.products_data = []; self.customers_data = {}; self.current_customer = None; self.image_dir = None
        self.load_config(); self.load_menu_data(); self.load_history(); self.load_customers()
        self._setup_styles(); self._create_widgets()
        if not self.image_dir or not os.path.isdir(self.image_dir): self.prompt_for_image_folder()
        self.populate_products(self.products_data)

    def exit_fullscreen(self, event=None): self.attributes('-fullscreen', False)

    def _setup_styles(self):
        self.style = ttk.Style(self); self.style.theme_use('clam')
        self.style.configure('Category.TButton', font=(FONT_FAMILY, 10), padding=5, background=FRAME_COLOR, foreground=FONT_COLOR)
        self.style.map('Category.TButton', background=[('active', ACCENT_COLOR)], foreground=[('active', FRAME_COLOR)])
        self.style.configure('History.TButton', font=(FONT_FAMILY, 10), padding=5, background='#e0e0e0', foreground=FONT_COLOR)
        self.style.map('History.TButton', background=[('active', '#c0c0c0')])
        self.style.configure('Action.TButton', font=(FONT_FAMILY, 11, 'bold'), padding=8, background='#007bff', foreground='white')
        self.style.map('Action.TButton', background=[('active', '#0056b3')])
        self.style.configure('Delete.TButton', font=(FONT_FAMILY, 11, 'bold'), padding=8, background='#dc3545', foreground='white')
        self.style.map('Delete.TButton', background=[('active', '#c82333')])
        self.style.configure('Payment.TButton', font=(FONT_FAMILY, 14, 'bold'), padding=20, background=ACCENT_COLOR, foreground=FONT_COLOR)
        self.style.map('Payment.TButton', background=[('active', '#bA9B74')])
        self.style.configure("Treeview.Heading", font=(FONT_FAMILY, 12, 'bold')); self.style.configure("Treeview", rowheight=25, font=(FONT_FAMILY, 11))

    def _create_widgets(self):
        menubar = tk.Menu(self); self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Keluar", command=self.destroy)
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Pengaturan", menu=settings_menu)
        settings_menu.add_command(label="Ubah Folder Gambar...", command=self.prompt_for_image_folder)
        settings_menu.add_separator()
        settings_menu.add_command(label="Tambah Menu Baru...", command=self.prompt_add_menu)
        main_scroll_frame = tk.Frame(self, bg=BG_COLOR); main_scroll_frame.pack(fill='both', expand=True)
        main_canvas = tk.Canvas(main_scroll_frame, bg=BG_COLOR, highlightthickness=0); main_scrollbar = ttk.Scrollbar(main_scroll_frame, orient="vertical", command=main_canvas.yview)
        content_frame = tk.Frame(main_canvas, bg=BG_COLOR)
        content_window = main_canvas.create_window((0, 0), window=content_frame, anchor="nw")
        main_canvas.bind('<Configure>', lambda e: main_canvas.itemconfig(content_window, width=e.width)); content_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.configure(yscrollcommand=main_scrollbar.set); main_canvas.pack(side="left", fill="both", expand=True); main_scrollbar.pack(side="right", fill="y")
        header_frame = tk.Frame(content_frame, bg=BG_COLOR); header_frame.pack(pady=10, fill='x'); tk.Label(header_frame, text="Selamat Datang di Kafe Kekinian!", font=(FONT_FAMILY, 22, "bold"), bg=BG_COLOR, fg=FONT_COLOR).pack()
        search_frame = tk.Frame(content_frame, bg=BG_COLOR); search_frame.pack(pady=(0, 10), padx=50, fill='x'); tk.Label(search_frame, text="🔍 Cari Menu:", font=(FONT_FAMILY, 12), bg=BG_COLOR).pack(side='left', padx=(0,10))
        self.search_entry = ttk.Entry(search_frame, font=(FONT_FAMILY, 12)); self.search_entry.pack(side='left', fill='x', expand=True); self.search_entry.bind('<KeyRelease>', self.on_search)
        category_frame = tk.Frame(content_frame, bg=BG_COLOR); category_frame.pack(pady=(0, 20), fill='x', padx=50)
        for text, cmd in [("Semua Menu", lambda: self.populate_products(self.products_data)), ("🍴 Makanan", lambda: self.filter_by_category("Makanan")), ("🥤 Minuman", lambda: self.filter_by_category("Minuman"))]:
            ttk.Button(category_frame, text=text, style='Category.TButton', command=cmd).pack(side='left', expand=True, fill='x', padx=5)
        ttk.Button(category_frame, text="📜 Riwayat Pesanan", style='History.TButton', command=self.show_history_window).pack(side='left', expand=True, fill='x', padx=5)
        paned_window = ttk.PanedWindow(content_frame, orient='horizontal'); paned_window.pack(fill='both', expand=True, padx=20, pady=10)
        product_container = tk.Frame(paned_window, bg=BG_COLOR); paned_window.add(product_container, weight=3)
        canvas_prod = tk.Canvas(product_container, bg=BG_COLOR, highlightthickness=0); scrollbar_prod = ttk.Scrollbar(product_container, orient="vertical", command=canvas_prod.yview)
        self.products_frame = tk.Frame(canvas_prod, bg=BG_COLOR); self.products_frame.bind("<Configure>", lambda e: canvas_prod.configure(scrollregion=canvas_prod.bbox("all")))
        prod_window = canvas_prod.create_window((0, 0), window=self.products_frame, anchor="nw")
        canvas_prod.bind('<Configure>', lambda e: canvas_prod.itemconfig(prod_window, width=e.width)); canvas_prod.configure(yscrollcommand=scrollbar_prod.set)
        canvas_prod.pack(side="left", fill="both", expand=True); scrollbar_prod.pack(side="right", fill="y")
        cart_main_frame = tk.Frame(paned_window, bg=FRAME_COLOR, relief='solid', borderwidth=1); paned_window.add(cart_main_frame, weight=2)
        customer_frame = tk.LabelFrame(cart_main_frame, text="Pelanggan", font=(FONT_FAMILY, 11, 'bold'), bg=FRAME_COLOR, padx=5, pady=5); customer_frame.pack(fill='x', padx=10, pady=(10,5))
        search_customer_frame = tk.Frame(customer_frame, bg=FRAME_COLOR); search_customer_frame.pack(fill='x'); tk.Label(search_customer_frame, text="No. HP:", font=(FONT_FAMILY, 10), bg=FRAME_COLOR).pack(side='left')
        self.customer_phone_entry = ttk.Entry(search_customer_frame, font=(FONT_FAMILY, 10)); self.customer_phone_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.find_customer_btn = ttk.Button(search_customer_frame, text="Cari", command=self.find_customer, width=5); self.find_customer_btn.pack(side='left')
        info_customer_frame = tk.Frame(customer_frame, bg=FRAME_COLOR); info_customer_frame.pack(fill='x', pady=5)
        self.customer_name_label = tk.Label(info_customer_frame, text="Pelanggan: -", font=(FONT_FAMILY, 10, 'bold'), bg=FRAME_COLOR, anchor='w'); self.customer_name_label.pack(fill='x')
        self.customer_points_label = tk.Label(info_customer_frame, text="Poin: -", font=(FONT_FAMILY, 10), bg=FRAME_COLOR, anchor='w'); self.customer_points_label.pack(fill='x')
        action_customer_frame = tk.Frame(customer_frame, bg=FRAME_COLOR); action_customer_frame.pack(fill='x', pady=(5,0))
        self.redeem_btn = ttk.Button(action_customer_frame, text="Gunakan Poin", command=self.redeem_points, state='disabled'); self.redeem_btn.pack(side='left', expand=True, fill='x', padx=(0,2))
        self.new_customer_btn = ttk.Button(action_customer_frame, text="Daftar Baru", command=self.register_customer); self.new_customer_btn.pack(side='left', expand=True, fill='x', padx=2)
        self.clear_customer_btn = ttk.Button(action_customer_frame, text="Lepas", command=self.clear_customer); self.clear_customer_btn.pack(side='left', expand=True, fill='x', padx=(2,0))
        tk.Label(cart_main_frame, text="🛒 Keranjang Belanja", font=(FONT_FAMILY, 16, "bold"), bg=FRAME_COLOR, fg=FONT_COLOR).pack(pady=(10,0), padx=10, anchor='w')
        cart_canvas_container = tk.Frame(cart_main_frame, bg=FRAME_COLOR); cart_canvas_container.pack(fill='both', expand=True, pady=5, padx=10)
        cart_canvas = tk.Canvas(cart_canvas_container, bg=FRAME_COLOR, highlightthickness=0); cart_scrollbar = ttk.Scrollbar(cart_canvas_container, orient="vertical", command=cart_canvas.yview)
        self.cart_items_frame = tk.Frame(cart_canvas, bg=FRAME_COLOR); self.cart_items_frame.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))
        cart_window = cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw")
        cart_canvas.bind('<Configure>', lambda e: cart_canvas.itemconfig(cart_window, width=e.width)); cart_canvas.configure(yscrollcommand=cart_scrollbar.set)
        cart_canvas.pack(side="left", fill="both", expand=True); cart_scrollbar.pack(side="right", fill="y")
        promo_frame = tk.Frame(cart_main_frame, bg=FRAME_COLOR); promo_frame.pack(fill='x', padx=10, pady=(5,0)); tk.Label(promo_frame, text="Kode Promo:", font=(FONT_FAMILY, 10), bg=FRAME_COLOR).pack(side='left')
        self.promo_entry = ttk.Entry(promo_frame, font=(FONT_FAMILY, 10)); self.promo_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.apply_promo_btn = ttk.Button(promo_frame, text="Terapkan", command=self.apply_promo, width=8); self.apply_promo_btn.pack(side='left')
        self.total_label = tk.Label(cart_main_frame, text="Subtotal: Rp0 (0 item)", font=(FONT_FAMILY, 12), bg=FRAME_COLOR, fg=FONT_COLOR); self.total_label.pack(anchor='w', padx=10, pady=(5,0))
        self.discount_label = tk.Label(cart_main_frame, text="", font=(FONT_FAMILY, 11, 'italic'), bg=FRAME_COLOR, fg='green'); self.discount_label.pack(anchor='w', padx=10)
        self.grand_total_label = tk.Label(cart_main_frame, text="Total Akhir: Rp0", font=(FONT_FAMILY, 14, "bold"), bg=FRAME_COLOR, fg=FONT_COLOR); self.grand_total_label.pack(anchor='w', padx=10)
        action_frame = tk.Frame(cart_main_frame, bg=FRAME_COLOR); action_frame.pack(fill='x', pady=15, padx=10)
        ttk.Button(action_frame, text="Kosongkan", style='Action.TButton', command=self.clear_cart).pack(side='left', expand=True, fill='x', padx=(0,5))
        ttk.Button(action_frame, text="Lanjutkan", style='Action.TButton', command=self.proceed_to_payment).pack(side='left', expand=True, fill='x', padx=(5,0))

    def prompt_add_menu(self):
        password = simpledialog.askstring("Otentikasi Admin", "Masukkan password admin:", show='*', parent=self)
        if password == ADMIN_PASSWORD:
            self.show_add_menu_window()
        elif password is not None:
            messagebox.showerror("Gagal", "Password salah. Anda tidak memiliki akses.", parent=self)

    def show_add_menu_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Tambah Menu Baru")
        add_window.geometry("450x550")
        add_window.configure(bg=BG_COLOR)
        add_window.transient(self)
        add_window.grab_set()
        main_frame = tk.Frame(add_window, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        tk.Label(main_frame, text="Form Tambah Menu Baru", font=(FONT_FAMILY, 16, 'bold'), bg=BG_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        labels = ["Nama Menu:", "Harga (Rp):", "Kategori:", "Stok Awal:", "Nama File Gambar:", "Deskripsi:"]
        for i, label_text in enumerate(labels):
            tk.Label(main_frame, text=label_text, font=(FONT_FAMILY, 11), bg=BG_COLOR).grid(row=i+1, column=0, sticky='w', pady=5)
        entry_name = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        entry_price = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        combo_category = ttk.Combobox(main_frame, values=["Makanan", "Minuman"], font=(FONT_FAMILY, 11), state='readonly')
        combo_category.set("Minuman")
        entry_stock = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        entry_image = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        text_desc = tk.Text(main_frame, font=(FONT_FAMILY, 11), height=5, width=30, wrap='word', relief='solid', borderwidth=1)
        entry_name.grid(row=1, column=1, sticky='ew', pady=5)
        entry_price.grid(row=2, column=1, sticky='ew', pady=5)
        combo_category.grid(row=3, column=1, sticky='ew', pady=5)
        entry_stock.grid(row=4, column=1, sticky='ew', pady=5)
        entry_image.grid(row=5, column=1, sticky='ew', pady=5)
        text_desc.grid(row=6, column=1, sticky='ew', pady=5)
        tk.Label(main_frame, text="(contoh: nama_gambar.png)", font=(FONT_FAMILY, 8, 'italic'), bg=BG_COLOR, fg='grey').grid(row=5, column=1, sticky='sw', padx=5)
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        save_btn = ttk.Button(button_frame, text="Simpan Menu", style='Action.TButton',
                              command=lambda: self.add_new_menu_item(
                                  add_window, entry_name, entry_price, combo_category,
                                  entry_stock, entry_image, text_desc
                              ))
        save_btn.pack(side='left', padx=10, fill='x', expand=True)
        cancel_btn = ttk.Button(button_frame, text="Batal", style='History.TButton', command=add_window.destroy)
        cancel_btn.pack(side='left', padx=10, fill='x', expand=True)
        main_frame.columnconfigure(1, weight=1)

    def add_new_menu_item(self, window, name_widget, price_widget, category_widget, stock_widget, image_widget, desc_widget):
        name = name_widget.get().strip()
        price_str = price_widget.get().strip()
        category = category_widget.get()
        stock_str = stock_widget.get().strip()
        image = image_widget.get().strip()
        desc = desc_widget.get("1.0", tk.END).strip()
        if not all([name, price_str, category, stock_str, image, desc]):
            messagebox.showerror("Error", "Semua kolom harus diisi.", parent=window)
            return
        try:
            price = int(price_str)
            stock = int(stock_str)
            if price <= 0 or stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus berupa angka positif.", parent=window)
            return
        if not image.lower().endswith(('.png', '.gif')):
             if not messagebox.askyesno("Peringatan Gambar", "Format gambar disarankan .png atau .gif.\nLanjutkan menyimpan?", parent=window):
                return
        new_id = max([p['id'] for p in self.products_data] or [0]) + 1
        new_product = {
            "id": new_id, "name": name, "price": price,
            "category": category, "desc": desc, "image": image, "stock": stock
        }
        self.products_data.append(new_product)
        self.save_menu_data()
        messagebox.showinfo("Berhasil", f"Menu '{name}' berhasil ditambahkan.", parent=window)
        self.refresh_product_display()
        window.destroy()

    def prompt_edit_menu(self, product, parent_window):
        """Meminta password sebelum membuka jendela edit."""
        password = simpledialog.askstring("Otentikasi Admin", "Masukkan password admin untuk mengubah menu:", show='*', parent=parent_window)
        if password == ADMIN_PASSWORD:
            parent_window.destroy()
            self.show_edit_menu_window(product)
        elif password is not None:
            messagebox.showerror("Gagal", "Password salah.", parent=parent_window)

    def show_edit_menu_window(self, product):
        """Menampilkan form untuk mengedit menu yang sudah ada, termasuk opsi hapus."""
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Edit Menu - {product['name']}")
        edit_window.geometry("450x600")
        edit_window.configure(bg=BG_COLOR)
        edit_window.transient(self)
        edit_window.grab_set()

        main_frame = tk.Frame(edit_window, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)

        tk.Label(main_frame, text="Form Edit Menu", font=(FONT_FAMILY, 16, 'bold'), bg=BG_COLOR).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        labels = ["Nama Menu:", "Harga (Rp):", "Kategori:", "Stok:", "Nama File Gambar:", "Deskripsi:"]
        for i, label_text in enumerate(labels):
            tk.Label(main_frame, text=label_text, font=(FONT_FAMILY, 11), bg=BG_COLOR).grid(row=i+1, column=0, sticky='w', pady=5)

        entry_name = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        entry_price = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        combo_category = ttk.Combobox(main_frame, values=["Makanan", "Minuman"], font=(FONT_FAMILY, 11), state='readonly')
        entry_stock = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        entry_image = ttk.Entry(main_frame, font=(FONT_FAMILY, 11))
        text_desc = tk.Text(main_frame, font=(FONT_FAMILY, 11), height=5, width=30, wrap='word', relief='solid', borderwidth=1)

        entry_name.insert(0, product['name'])
        entry_price.insert(0, product['price'])
        combo_category.set(product['category'])
        entry_stock.insert(0, product.get('stock', 0))
        entry_image.insert(0, product['image'])
        text_desc.insert('1.0', product['desc'])

        entry_name.grid(row=1, column=1, sticky='ew', pady=5)
        entry_price.grid(row=2, column=1, sticky='ew', pady=5)
        combo_category.grid(row=3, column=1, sticky='ew', pady=5)
        entry_stock.grid(row=4, column=1, sticky='ew', pady=5)
        entry_image.grid(row=5, column=1, sticky='ew', pady=5)
        text_desc.grid(row=6, column=1, sticky='ew', pady=5)
        
        button_frame = tk.Frame(main_frame, bg=BG_COLOR)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))

        save_btn = ttk.Button(button_frame, text="Simpan Perubahan", style='Action.TButton',
                              command=lambda: self.save_menu_edits(
                                  product['id'], edit_window, entry_name, entry_price, combo_category,
                                  entry_stock, entry_image, text_desc
                              ))
        save_btn.pack(pady=5, fill='x')

        delete_btn = ttk.Button(button_frame, text="Hapus Menu Ini", style='Delete.TButton',
                                command=lambda: self.delete_menu_item(product, edit_window))
        delete_btn.pack(pady=(10, 5), fill='x')
        
        cancel_btn = ttk.Button(button_frame, text="Batal", style='History.TButton', command=edit_window.destroy)
        cancel_btn.pack(pady=(5,0), fill='x')

        main_frame.columnconfigure(1, weight=1)
        
    def save_menu_edits(self, product_id, window, name_widget, price_widget, category_widget, stock_widget, image_widget, desc_widget):
        name = name_widget.get().strip()
        price_str = price_widget.get().strip()
        stock_str = stock_widget.get().strip()
        if not all([name, price_str, stock_str]):
            messagebox.showerror("Error", "Nama, Harga, dan Stok tidak boleh kosong.", parent=window)
            return
        try:
            price = int(price_str)
            stock = int(stock_str)
            if price <= 0 or stock < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Harga dan Stok harus berupa angka positif.", parent=window)
            return

        product_to_update = self.get_product_by_id(product_id)
        if product_to_update:
            product_to_update['name'] = name
            product_to_update['price'] = price
            product_to_update['category'] = category_widget.get()
            product_to_update['stock'] = stock
            product_to_update['image'] = image_widget.get().strip()
            product_to_update['desc'] = desc_widget.get("1.0", tk.END).strip()
            
            self.save_menu_data()
            messagebox.showinfo("Berhasil", f"Menu '{name}' telah berhasil diperbarui.", parent=window)
            
            window.destroy()
            self.refresh_product_display()
            self.update_cart_display()
        else:
            messagebox.showerror("Error", "Produk tidak ditemukan untuk diperbarui.", parent=window)

    def delete_menu_item(self, product_to_delete, parent_window):
        """Menangani logika penghapusan menu, dipanggil dari dalam jendela Edit."""
        if product_to_delete['id'] in self.cart:
            messagebox.showerror("Gagal Menghapus", 
                                 "Item ini sedang ada di keranjang belanja.\n"
                                 "Kosongkan keranjang terlebih dahulu untuk menghapus item ini.", 
                                 parent=parent_window)
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Anda yakin ingin menghapus menu '{product_to_delete['name']}' secara permanen?\n\n"
            "Tindakan ini tidak dapat diurungkan.",
            icon='warning',
            parent=parent_window
        )

        if confirm:
            self.products_data = [p for p in self.products_data if p['id'] != product_to_delete['id']]
            self.save_menu_data()
            parent_window.destroy()
            self.refresh_product_display()
            messagebox.showinfo("Berhasil", f"Menu '{product_to_delete['name']}' telah berhasil dihapus.")

    def finalize_transaction(self, window_to_close, payment_method):
        subtotal = sum(item['qty'] * item['price'] for item in self.cart.values()); discount, promo_code = 0, None
        if self.applied_promo:
            promo_code = self.applied_promo['code']
            if self.applied_promo['type'] == 'percent': discount = (self.applied_promo['value'] / 100) * subtotal
            elif self.applied_promo['type'] == 'fixed': discount = self.applied_promo['value']
        discount = min(discount, subtotal); final_price_after_promo = subtotal - discount
        points_discount = min(self.points_redeemed * NILAI_POIN_RP, final_price_after_promo)
        final_price = final_price_after_promo - points_discount
        customer_id = self.current_customer['phone'] if self.current_customer else None
        points_earned = math.floor(final_price / POIN_PER_RP)
        transaction = {"id": datetime.now().strftime("%Y%m%d%H%M%S"), "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "items": list(self.cart.values()), "subtotal": subtotal, "discount": discount, "promo_code": promo_code, "points_redeemed_value": points_discount, "total_price": final_price, "payment_method": payment_method, "customer_id": customer_id, "points_earned": points_earned }
        self.transaction_history.append(transaction); self.save_history()
        if self.current_customer:
            self.customers_data[customer_id]['points'] -= self.points_redeemed
            self.customers_data[customer_id]['points'] += points_earned
            self.save_customers()
        window_to_close.destroy()
        messagebox.showinfo("Transaksi Berhasil", "Pembayaran telah diterima. Terima kasih!")
        self.clear_cart()

    def clear_cart(self):
        if not self.cart and not self.current_customer and not self.applied_promo and self.points_redeemed == 0: return
        if self.cart:
            if messagebox.askyesno("Konfirmasi", "Anda yakin ingin mengosongkan keranjang dan mereset transaksi?"):
                for prod_id, item in self.cart.items():
                    product_in_db = self.get_product_by_id(prod_id)
                    if product_in_db:
                        product_in_db['stock'] += item['qty']
                self.save_menu_data()
                self.cart.clear()
            else:
                return
        self.remove_promo()
        self.clear_customer()
        self.refresh_product_display()
    
    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f: self.image_dir = json.load(f).get("image_directory")
        except (json.JSONDecodeError, FileNotFoundError): self.image_dir = None
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f: json.dump({"image_directory": self.image_dir}, f, indent=4)
    
    def prompt_for_image_folder(self):
        messagebox.showinfo("Pilih Folder Gambar", "Silakan pilih folder 'Kafe_Menu' tempat Anda menyimpan semua gambar produk.")
        selected_directory = filedialog.askdirectory(title="Pilih Folder Kafe_Menu Anda")
        if selected_directory:
            self.image_dir = selected_directory
            self.save_config()
            messagebox.showinfo("Berhasil", f"Folder gambar telah diatur ke:\n{self.image_dir}")
            self.image_cache.clear()
            self.populate_products(self.products_data)
        else:
            messagebox.showwarning("Peringatan", "Folder gambar tidak dipilih. Gambar tidak akan ditampilkan.")
            
    def load_menu_data(self):
        try:
            if os.path.exists(MENU_DATA_FILE):
                with open(MENU_DATA_FILE, 'r') as f: self.products_data = json.load(f)
            else: self.products_data = initial_data_products; self.save_menu_data()
        except (json.JSONDecodeError, FileNotFoundError): self.products_data = initial_data_products; self.save_menu_data()
        
    def save_menu_data(self):
        with open(MENU_DATA_FILE, 'w') as f: json.dump(self.products_data, f, indent=4)
        
    def get_product_by_id(self, product_id):
        return next((p for p in self.products_data if p['id'] == product_id), None)
        
    def get_image(self, image_name, size='product'):
        if not self.image_dir: return None
        factor = 4 if size == 'detail' else (4 if size == 'product' else 10)
        cache_key = f"{image_name}_{size}"
        if cache_key in self.image_cache: return self.image_cache[cache_key]
        path = os.path.join(self.image_dir, image_name)
        if not os.path.exists(path): return None
        try:
            img = PhotoImage(file=path)
            small_img = img.subsample(factor, factor)
            self.image_cache[cache_key] = small_img
            return small_img
        except tk.TclError:
            return None
            
    def on_search(self, event=None):
        query = self.search_entry.get().lower().strip()
        if not query:
            self.populate_products(self.products_data)
        else:
            filtered_products = [p for p in self.products_data if query in p['name'].lower()]
            self.populate_products(filtered_products)
            
    def populate_products(self, products):
        for widget in self.products_frame.winfo_children(): widget.destroy()
        self.products_frame.columnconfigure(0, weight=1); self.products_frame.columnconfigure(1, weight=1)
        for i, product in enumerate(products):
            row, col = divmod(i, 2)
            card = tk.Frame(self.products_frame, bg=FRAME_COLOR, relief='raised', borderwidth=1)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
            is_out_of_stock = self.get_product_by_id(product['id']).get('stock', 0) <= 0
            img_container = tk.Frame(card, bg=FRAME_COLOR, cursor="hand2")
            img_container.pack(padx=10, pady=10)
            img = self.get_image(product["image"], size='product')
            img_label = tk.Label(img_container, bg=FRAME_COLOR, cursor="hand2")
            if img:
                img_label.config(image=img)
                img_label.image = img
            else:
                img_label.config(text=f"[No Img:\n{product['image']}]", font=(FONT_FAMILY, 8), width=15, height=8, fg='grey', bg='#eee')
            img_label.grid(row=0, column=0)
            if is_out_of_stock:
                sold_out_label = tk.Label(img_container, text="STOK HABIS", font=(FONT_FAMILY, 14, 'bold'), bg='red', fg='white', relief='solid', bd=1)
                sold_out_label.grid(row=0, column=0, sticky="nsew")
                img_label.config(bg='#cccccc')
            name_label = tk.Label(card, text=product["name"], font=(FONT_FAMILY, 12, "bold"), bg=FRAME_COLOR, fg=FONT_COLOR, cursor="hand2")
            name_label.pack(padx=10, fill='x')
            tk.Label(card, text=f"Rp{product['price']:,}", font=(FONT_FAMILY, 11), bg=FRAME_COLOR, fg=FONT_COLOR).pack(padx=10)
            tk.Label(card, text=f"Stok: {product.get('stock', 0)}", font=(FONT_FAMILY, 10, 'italic'), bg=FRAME_COLOR, fg=FONT_COLOR).pack(padx=10)
            for w in [img_container, img_label, name_label]:
                w.bind("<Button-1>", lambda e, p=product: self.show_product_details(p))
            btn_frame = tk.Frame(card, bg=FRAME_COLOR); btn_frame.pack(pady=10)
            btn_minus = tk.Button(btn_frame, text="-", font=(FONT_FAMILY, 12), bg="#E06C75", fg="white", width=2, relief='flat', command=lambda p=product: self.remove_from_cart(p))
            btn_minus.pack(side='left', padx=5)
            btn_plus = tk.Button(btn_frame, text="+", font=(FONT_FAMILY, 12), bg="#98C379", fg="white", width=2, relief='flat', command=lambda p=product: self.add_to_cart(p))
            btn_plus.pack(side='left', padx=5)
            if is_out_of_stock: btn_plus.config(state='disabled')
            
    def filter_by_category(self, category):
        filtered_products = [p for p in self.products_data if p['category'] == category]
        self.populate_products(filtered_products)
        
    def add_to_cart(self, product):
        prod_id = product['id']
        product_in_db = self.get_product_by_id(prod_id)
        if not product_in_db or product_in_db.get('stock', 0) <= 0:
            messagebox.showwarning("Stok Habis", f"Maaf, stok untuk {product['name']} sudah habis.")
            return
        product_in_db['stock'] -= 1
        if prod_id in self.cart:
            self.cart[prod_id]['qty'] += 1
        else:
            self.cart[prod_id] = {'id': prod_id, 'name': product['name'], 'price': product['price'], 'qty': 1, 'image': product['image']}
        self.save_menu_data()
        self.update_cart_display()
        self.refresh_product_display()
        
    def remove_from_cart(self, product):
        prod_id = product['id']
        if prod_id in self.cart:
            product_in_db = self.get_product_by_id(prod_id)
            if product_in_db: product_in_db['stock'] += 1
            self.cart[prod_id]['qty'] -= 1
            if self.cart[prod_id]['qty'] == 0:
                del self.cart[prod_id]
            self.save_menu_data()
            self.update_cart_display()
            self.refresh_product_display()
            
    def refresh_product_display(self):
        self.on_search()
        
    def update_cart_display(self):
        for widget in self.cart_items_frame.winfo_children(): widget.destroy()
        subtotal, total_items = 0, 0
        for item in sorted(self.cart.values(), key=lambda x: x['name']):
            item_subtotal = item['qty'] * item['price']
            item_card = tk.Frame(self.cart_items_frame, bg='#FAFAFA', relief='solid', bd=1)
            item_card.pack(fill='x', pady=4, padx=4)
            img = self.get_image(item['image'], size='cart')
            img_label = tk.Label(item_card, bg='#FAFAFA')
            if img:
                img_label.config(image=img)
                img_label.image = img
            else:
                img_label.config(text="[x]", font=(FONT_FAMILY, 8), fg='grey', bg='#eee')
            img_label.pack(side='left', padx=5, pady=5)
            detail_frame = tk.Frame(item_card, bg='#FAFAFA')
            detail_frame.pack(side='left', fill='x', expand=True, padx=5)
            tk.Label(detail_frame, text=f"{item['name']} x{item['qty']}", font=(FONT_FAMILY, 10, 'bold'), anchor='w', bg='#FAFAFA').pack(fill='x')
            tk.Label(detail_frame, text=f"Rp{item_subtotal:,}", font=(FONT_FAMILY, 9), anchor='w', bg='#FAFAFA').pack(fill='x')
            subtotal += item_subtotal
            total_items += item['qty']

        discount_amount = 0
        self.discount_label.config(text="")
        if self.applied_promo and subtotal > 0:
            if self.applied_promo['type'] == 'percent':
                discount_amount = (self.applied_promo['value'] / 100) * subtotal
            elif self.applied_promo['type'] == 'fixed':
                discount_amount = self.applied_promo['value']
            discount_amount = min(discount_amount, subtotal)
            self.discount_label.config(text=f"Diskon ({self.applied_promo['code']}): -Rp{discount_amount:,.0f}")

        grand_total = subtotal - discount_amount
        points_discount = 0
        if self.points_redeemed > 0:
            points_discount = self.points_redeemed * NILAI_POIN_RP
            points_discount = min(points_discount, grand_total)
            current_discount_text = self.discount_label.cget("text")
            new_discount_text = (current_discount_text + " | " if current_discount_text else "") + f"Poin: -Rp{points_discount:,.0f}"
            self.discount_label.config(text=new_discount_text)
            
        final_total = grand_total - points_discount
        self.total_label.config(text=f"Subtotal: Rp{subtotal:,} ({total_items} item)")
        self.grand_total_label.config(text=f"Total Akhir: Rp{final_total:,.0f}")
        
    def apply_promo(self):
        if self.points_redeemed > 0:
            messagebox.showwarning("Peringatan", "Lepas diskon poin terlebih dahulu untuk menggunakan promo.")
            return
        promo_code = self.promo_entry.get().upper().strip()
        if not promo_code: return
        if promo_code in VALID_PROMOS:
            self.applied_promo = {"code": promo_code, **VALID_PROMOS[promo_code]}
            messagebox.showinfo("Promo Berhasil", f"Kode promo '{promo_code}' berhasil diterapkan!")
            self.promo_entry.config(state='disabled')
            self.apply_promo_btn.config(text="Hapus", command=self.remove_promo)
        else:
            messagebox.showerror("Promo Gagal", f"Kode promo '{promo_code}' tidak valid.")
            self.applied_promo = None
        self.update_cart_display()
        
    def remove_promo(self):
        if self.applied_promo:
            self.applied_promo = None
            self.promo_entry.config(state='normal')
            self.promo_entry.delete(0, tk.END)
            self.apply_promo_btn.config(text="Terapkan", command=self.apply_promo)
            self.update_cart_display()
            
    def proceed_to_payment(self):
        if not self.cart:
            messagebox.showwarning("Keranjang Kosong", "Silakan tambahkan item.")
            return
        subtotal = sum(item['qty'] * item['price'] for item in self.cart.values())
        discount = 0
        if self.applied_promo:
            if self.applied_promo['type'] == 'percent':
                discount = (self.applied_promo['value'] / 100) * subtotal
            elif self.applied_promo['type'] == 'fixed':
                discount = self.applied_promo['value']
        discount = min(discount, subtotal)
        final_price_after_promo = subtotal - discount
        points_discount = min(self.points_redeemed * NILAI_POIN_RP, final_price_after_promo)
        final_price = final_price_after_promo - points_discount

        payment_window = tk.Toplevel(self)
        payment_window.title("Pilih Metode Pembayaran")
        payment_window.geometry("600x300")
        payment_window.configure(bg=BG_COLOR)
        payment_window.transient(self)
        payment_window.grab_set()
        
        tk.Label(payment_window, text="Metode Pembayaran", font=(FONT_FAMILY, 18, 'bold'), bg=BG_COLOR).pack(pady=20)
        tk.Label(payment_window, text=f"Total Tagihan: Rp{final_price:,.0f}", font=(FONT_FAMILY, 14), bg=BG_COLOR).pack(pady=(0, 20))
        btn_frame = tk.Frame(payment_window, bg=BG_COLOR)
        btn_frame.pack(fill='x', padx=20)
        
        ttk.Button(btn_frame, text="💵 Tunai", style='Payment.TButton', command=lambda: self.show_cash_payment(final_price, payment_window)).pack(side='left', expand=True, padx=10)
        ttk.Button(btn_frame, text="💳 Non-Tunai", style='Payment.TButton', command=lambda: self.show_non_cash_payment(final_price, payment_window)).pack(side='left', expand=True, padx=10)
        
    def show_cash_payment(self, total_price, parent_window):
        parent_window.destroy()
        cash_window = tk.Toplevel(self)
        cash_window.title("Pembayaran Tunai")
        cash_window.geometry("400x250")
        cash_window.configure(bg=FRAME_COLOR)
        cash_window.transient(self)
        cash_window.grab_set()
        tk.Label(cash_window, text=f"Total Pembayaran:\nRp{total_price:,.0f}", font=(FONT_FAMILY, 20, 'bold'), bg=FRAME_COLOR).pack(pady=20)
        tk.Label(cash_window, text="Silakan membayar ke kasir, terima kasih.", font=(FONT_FAMILY, 14), wraplength=350, bg=FRAME_COLOR).pack(pady=10)
        ttk.Button(cash_window, text="Selesai", style='Action.TButton', command=lambda: self.finalize_transaction(cash_window, "Tunai")).pack(pady=20, padx=20, fill='x')
        
    def show_non_cash_payment(self, total_price, parent_window):
        parent_window.destroy(); non_cash_window = tk.Toplevel(self); non_cash_window.title("Pembayaran Non-Tunai"); non_cash_window.geometry("400x300"); non_cash_window.configure(bg=FRAME_COLOR); non_cash_window.transient(self); non_cash_window.grab_set()
        tk.Label(non_cash_window, text=f"Total Pembayaran:\nRp{total_price:,.0f}", font=(FONT_FAMILY, 18, 'bold'), bg=FRAME_COLOR).pack(pady=25)
        tk.Label(non_cash_window, text="Silakan transfer ke nomor rekening:", font=(FONT_FAMILY, 12), bg=FRAME_COLOR).pack(pady=(15, 0))
        tk.Label(non_cash_window, text="123-456-7890 (Bank Kafe Kekinian)", font=(FONT_FAMILY, 14, 'bold'), bg=FRAME_COLOR).pack(pady=5)
        ttk.Button(non_cash_window, text="Selesai", style='Action.TButton', command=lambda: self.finalize_transaction(non_cash_window, "Non-Tunai")).pack(pady=25, padx=20, fill='x')

    def save_history(self):
        with open(HISTORY_FILE, 'w') as f: json.dump(self.transaction_history, f, indent=4)
        
    def load_history(self):
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f: self.transaction_history = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): self.transaction_history = []
        
    def show_history_window(self):
        history_window = tk.Toplevel(self); history_window.title("Riwayat Transaksi"); history_window.geometry("900x600"); history_window.configure(bg=BG_COLOR); history_window.transient(self); history_window.grab_set()
        main_frame = tk.Frame(history_window, bg=BG_COLOR, padx=10, pady=10); main_frame.pack(fill='both', expand=True)
        tree_frame = tk.Frame(main_frame); tree_frame.pack(fill='both', expand=True, pady=(0,5))
        cols = ("ID Transaksi", "Waktu", "Pelanggan", "Total Harga", "Metode Bayar"); self.history_tree = ttk.Treeview(tree_frame, columns=cols, show='headings', style="Treeview")
        for col in cols: self.history_tree.heading(col, text=col); self.history_tree.column(col, width=150, anchor='w')
        for trx in reversed(self.transaction_history):
            customer_name = self.customers_data.get(trx.get('customer_id', ''), {}).get('name', 'N/A')
            self.history_tree.insert("", "end", iid=trx['id'], values=(trx['id'], trx['timestamp'], customer_name, f"Rp{trx['total_price']:,.0f}", trx['payment_method']))
        self.history_tree.pack(side='left', fill='both', expand=True); scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.history_tree.yview); self.history_tree.configure(yscrollcommand=scrollbar.set); scrollbar.pack(side='right', fill='y')
        detail_frame = tk.Frame(main_frame, bg=FRAME_COLOR, bd=1, relief='sunken'); detail_frame.pack(fill='x', pady=(5,0)); tk.Label(detail_frame, text="Detail Transaksi", font=(FONT_FAMILY, 14, 'bold'), bg=FRAME_COLOR).pack(pady=5)
        self.detail_text = tk.Text(detail_frame, height=10, font=(FONT_FAMILY, 11), state='disabled', bg=FRAME_COLOR, relief='flat', wrap='word'); self.detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        def show_details(event):
            selected_id = self.history_tree.focus()
            if not selected_id: return
            selected_trx = next((trx for trx in self.transaction_history if trx['id'] == selected_id), None)
            self.detail_text.config(state='normal'); self.detail_text.delete('1.0', tk.END)
            if selected_trx:
                customer_name = self.customers_data.get(selected_trx.get('customer_id', ''), {}).get('name', 'Umum')
                header = f"ID: {selected_trx['id']} | Waktu: {selected_trx['timestamp']} | Pelanggan: {customer_name}\n"; self.detail_text.insert(tk.END, header, 'bold')
                self.detail_text.insert(tk.END, "-"*80 + "\n\n"); self.detail_text.insert(tk.END, "Item yang Dipesan:\n", 'bold')
                for item in selected_trx['items']: self.detail_text.insert(tk.END, f"  - {item['name']} x{item['qty']} (Rp{item['price']*item['qty']:,})\n")
                self.detail_text.insert(tk.END, "\n" + "-"*80 + "\n"); self.detail_text.insert(tk.END, "Ringkasan Pembayaran:\n", 'bold')
                self.detail_text.insert(tk.END, f"  Subtotal: Rp{selected_trx['subtotal']:,}\n")
                if selected_trx.get('promo_code'): self.detail_text.insert(tk.END, f"  Diskon ({selected_trx['promo_code']}): -Rp{selected_trx['discount']:,.0f}\n", 'italic')
                if selected_trx.get('points_redeemed_value', 0) > 0: self.detail_text.insert(tk.END, f"  Diskon Poin: -Rp{selected_trx['points_redeemed_value']:,}\n", 'italic')
                self.detail_text.insert(tk.END, f"  Total Akhir: Rp{selected_trx['total_price']:,.0f}\n", 'bold')
                self.detail_text.insert(tk.END, f"  Metode Bayar: {selected_trx['payment_method']}\n"); self.detail_text.insert(tk.END, f"  Poin Didapat: +{selected_trx.get('points_earned', 0)} poin\n")
            self.detail_text.tag_configure('bold', font=(FONT_FAMILY, 11, 'bold')); self.detail_text.tag_configure('italic', font=(FONT_FAMILY, 11, 'italic'), foreground='green'); self.detail_text.config(state='disabled')
        self.history_tree.bind("<<TreeviewSelect>>", show_details)
        
    def show_product_details(self, product):
        detail_window = tk.Toplevel(self)
        detail_window.title(f"Detail - {product['name']}")
        detail_window.geometry("500x600")
        detail_window.configure(bg=FRAME_COLOR)
        detail_window.transient(self)
        detail_window.grab_set()

        img_frame = tk.Frame(detail_window, bg=FRAME_COLOR)
        img_frame.pack(pady=20)
        detail_img = self.get_image(product['image'], size='detail')
        if detail_img:
            img_label = tk.Label(img_frame, image=detail_img, bg=FRAME_COLOR)
            img_label.image = detail_img
            img_label.pack()

        tk.Label(detail_window, text=product['name'], font=(FONT_FAMILY, 20, 'bold'), bg=FRAME_COLOR, fg=FONT_COLOR).pack(pady=(0,5))
        tk.Label(detail_window, text=f"Rp{product['price']:,}", font=(FONT_FAMILY, 16), bg=FRAME_COLOR, fg=FONT_COLOR).pack(pady=(0, 15))

        desc_frame = tk.Frame(detail_window, bg=BG_COLOR, bd=1, relief='sunken')
        desc_frame.pack(fill='both', expand=True, padx=20, pady=10)
        desc_text = tk.Text(desc_frame, font=(FONT_FAMILY, 11), wrap='word', relief='flat', bg=BG_COLOR, height=8)
        desc_text.insert('1.0', product['desc'])
        desc_text.config(state='disabled')
        desc_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        is_out_of_stock = self.get_product_by_id(product['id']).get('stock', 0) <= 0
        
        action_frame_detail = tk.Frame(detail_window, bg=FRAME_COLOR)
        action_frame_detail.pack(pady=20, padx=20, fill='x')
        
        btn_add = ttk.Button(action_frame_detail, text="Tambah ke Keranjang", style='Action.TButton', command=lambda: [self.add_to_cart(product), detail_window.destroy()])
        btn_add.pack(side='left', expand=True, fill='x', padx=(0,5))
        if is_out_of_stock: btn_add.config(state='disabled')

        # Tombol "Ubah / Hapus Menu" sebagai pengganti tombol hapus dan tutup yang terpisah
        btn_edit = ttk.Button(action_frame_detail, text="Ubah / Hapus Menu", style='Action.TButton', command=lambda: self.prompt_edit_menu(product, detail_window))
        btn_edit.pack(side='left', expand=True, fill='x', padx=5)

        ttk.Button(action_frame_detail, text="Tutup", style='History.TButton', command=detail_window.destroy).pack(side='left', expand=True, fill='x', padx=(5,0))

    def load_customers(self):
        try:
            if os.path.exists(CUSTOMERS_FILE):
                with open(CUSTOMERS_FILE, 'r') as f: self.customers_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError): self.customers_data = {}
        
    def save_customers(self):
        with open(CUSTOMERS_FILE, 'w') as f: json.dump(self.customers_data, f, indent=4)
        
    def find_customer(self):
        phone = self.customer_phone_entry.get().strip()
        if not phone: return
        customer = self.customers_data.get(phone)
        if customer:
            self.current_customer = {"phone": phone, **customer}
            self.update_customer_panel()
        else:
            messagebox.showinfo("Tidak Ditemukan", f"Pelanggan dengan No. HP {phone} tidak ditemukan.")
            self.clear_customer()
            
    def register_customer(self):
        phone = simpledialog.askstring("Pelanggan Baru", "Masukkan No. HP Pelanggan:", parent=self)
        if not phone: return
        if phone in self.customers_data:
            messagebox.showerror("Gagal", "No. HP sudah terdaftar.")
            return
        name = simpledialog.askstring("Pelanggan Baru", "Masukkan Nama Pelanggan:", parent=self)
        if not name: return
        self.customers_data[phone] = {"name": name, "points": 0}
        self.save_customers()
        self.current_customer = {"phone": phone, "name": name, "points": 0}
        self.update_customer_panel()
        messagebox.showinfo("Berhasil", f"Pelanggan '{name}' berhasil didaftarkan.")
        
    def clear_customer(self):
        self.current_customer = None
        self.update_customer_panel()
        
    def update_customer_panel(self):
        if self.current_customer:
            self.customer_name_label.config(text=f"Pelanggan: {self.current_customer['name']}")
            self.customer_points_label.config(text=f"Poin: {self.current_customer['points']}")
            self.customer_phone_entry.delete(0, tk.END)
            self.customer_phone_entry.insert(0, self.current_customer['phone'])
            self.customer_phone_entry.config(state='disabled')
            self.find_customer_btn.config(state='disabled')
            self.redeem_btn.config(state='normal' if self.current_customer['points'] > 0 else 'disabled')
        else:
            self.customer_name_label.config(text="Pelanggan: -")
            self.customer_points_label.config(text="Poin: -")
            self.customer_phone_entry.config(state='normal')
            self.customer_phone_entry.delete(0, tk.END)
            self.find_customer_btn.config(state='normal')
            self.redeem_btn.config(state='disabled')
        self.points_redeemed = 0
        self.update_cart_display()
        
    def redeem_points(self):
        if not self.current_customer: return
        if self.applied_promo:
            messagebox.showwarning("Peringatan", "Lepas promo terlebih dahulu untuk menggunakan poin.")
            return
        points_to_use_str = simpledialog.askstring("Gunakan Poin", f"Anda memiliki {self.current_customer['points']} poin. (1 poin = Rp{NILAI_POIN_RP})\nBerapa poin yang ingin digunakan?", parent=self)
        if not points_to_use_str: return
        try:
            points_to_use = int(points_to_use_str)
            if 0 < points_to_use <= self.current_customer['points']:
                self.points_redeemed = points_to_use
                self.update_cart_display()
            else:
                messagebox.showerror("Error", "Jumlah poin tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid.")

if __name__ == "__main__":
    app = CafeApp()
    app.mainloop()