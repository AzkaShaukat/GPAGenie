import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from app.services.blog_service import create_post, update_post
from app.utils.exceptions import BlogError
import os

class BlogPostForm:
    def __init__(self, parent_frame, user, blog_manager, mode, post=None):
        self.parent = parent_frame
        self.user = user
        self.blog_manager = blog_manager
        self.mode = mode
        self.post = post
        self.image_path = None
        self.image_preview = None

        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff", width=700)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.text = tk.Text(self.main_frame, bg="#f0f8ff", relief="flat", highlightthickness=0, width=70)
        self.text.pack(fill="both", expand=True)

        self.form_frame = tk.Frame(self.text, bg="#f0f8ff")
        self.text.window_create("end", window=self.form_frame)
        self.form_frame.pack(expand=True)

        self.setup_form()

        if mode == "edit" and post:
            self.load_post_data()

    def setup_form(self):
        ttk.Button(self.form_frame, text="← Back to Manager", command=self.go_back, style="TButton").pack(anchor="w", pady=(0, 20))
        tk.Label(self.form_frame, text="Edit Post" if self.mode == "edit" else "Create New Post", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#4b0082").pack(anchor="w", pady=(0, 20))

        fields_frame = tk.Frame(self.form_frame, bg="#f0f8ff")
        fields_frame.pack(fill="x", expand=True)

        left_col = tk.Frame(fields_frame, bg="#f0f8ff", padx=10)
        left_col.pack(side="left", fill="both", expand=True)

        tk.Label(left_col, text="Title:", font=("Helvetica", 12), bg="#f0f8ff").pack(anchor="w", pady=(0, 5))
        self.title_entry = ttk.Entry(left_col, font=("Helvetica", 12), width=50)
        self.title_entry.pack(fill="x", pady=(0, 15))

        tk.Label(left_col, text="Excerpt:", font=("Helvetica", 12), bg="#f0f8ff").pack(anchor="w", pady=(0, 5))
        self.excerpt_text = tk.Text(left_col, font=("Helvetica", 12), height=4, wrap="word", padx=5, pady=5)
        self.excerpt_text.pack(fill="x", pady=(0, 15))

        tk.Label(left_col, text="Content:", font=("Helvetica", 12), bg="#f0f8ff").pack(anchor="w", pady=(0, 5))
        self.content_text = tk.Text(left_col, font=("Helvetica", 12), height=15, wrap="word", padx=5, pady=5)
        self.content_text.pack(fill="x", pady=(0, 15))

        image_frame = tk.Frame(left_col, bg="#f0f8ff")
        image_frame.pack(fill="x", pady=(10, 0))

        tk.Label(image_frame, text="Featured Image:", font=("Helvetica", 12), bg="#f0f8ff").pack(anchor="w", pady=(0, 5))
        self.image_display_frame = tk.Frame(image_frame, bg="white", bd=1, relief="solid")
        self.image_display_frame.pack(fill="x", pady=(0, 10))

        self.image_label = tk.Label(self.image_display_frame, text="No image selected", font=("Helvetica", 10), bg="white", fg="#666666", width=30, height=10)
        self.image_label.pack(padx=10, pady=10)

        btn_frame = tk.Frame(image_frame, bg="#f0f8ff")
        btn_frame.pack(fill="x")

        ttk.Button(btn_frame, text="Select Image", command=self.select_image).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Remove Image", command=self.remove_image, style="Danger.TButton").pack(side="left")

        if self.mode == "edit":
            status_frame = tk.Frame(left_col, bg="#f0f8ff")
            status_frame.pack(fill="x", pady=(10, 0))
            tk.Label(status_frame, text="Status:", font=("Helvetica", 12), bg="#f0f8ff").pack(side="left", padx=(0, 10))
            self.status_var = tk.StringVar(value="published")
            ttk.Combobox(status_frame, textvariable=self.status_var, values=["published", "draft", "archived"], state="readonly", width=15).pack(side="left")

        submit_btn = ttk.Button(self.form_frame, text="Save Post", command=self.submit_form, style="Accent.TButton", width=20)
        submit_btn.pack(pady=20)

    def load_post_data(self):
        self.title_entry.insert(0, self.post['title'])
        self.excerpt_text.insert("1.0", self.post['excerpt'])
        self.content_text.insert("1.0", self.post['content'])
        if self.post.get('status'):
            self.status_var.set(self.post['status'])
        if self.post.get('featured_image'):
            self.image_path = self.post['featured_image']
            self.update_image_preview()

    def select_image(self):
        filetypes = (("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*"))
        filename = filedialog.askopenfilename(title="Select featured image", initialdir=os.path.expanduser("~"), filetypes=filetypes)
        if filename:
            self.image_path = filename
            self.update_image_preview()

    def remove_image(self):
        self.image_path = None
        self.image_label.config(image="", text="No image selected")
        if hasattr(self, 'image_preview'):
            del self.image_preview

    def update_image_preview(self):
        try:
            img = Image.open(self.image_path)
            img.thumbnail((200, 200))
            self.image_preview = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.image_preview, text="")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            self.remove_image()

    def submit_form(self):
        title = self.title_entry.get().strip()
        excerpt = self.excerpt_text.get("1.0", "end-1c").strip()
        content = self.content_text.get("1.0", "end-1c").strip()

        if not title:
            messagebox.showwarning("Warning", "Please enter a title")
            return
        if not content:
            messagebox.showwarning("Warning", "Please enter content")
            return

        try:
            post_data = {
                'title': title,
                'excerpt': excerpt,
                'content': content,
                'featured_image': self.image_path,
                'author_id': 1  # Hardcoded to 1 for the admin
            }

            if self.mode == "edit":
                post_data['post_id'] = self.post['post_id']
                if hasattr(self, 'status_var'):
                    post_data['status'] = self.status_var.get()
                update_post(post_data)
                messagebox.showinfo("Success", "Post updated successfully")
            else:
                create_post(post_data)
                messagebox.showinfo("Success", "Post created successfully")

            self.go_back()

        except BlogError as e:
            messagebox.showerror("Error", f"Failed to save post: {str(e)}")

    def go_back(self):
        self.main_frame.pack_forget()
        self.blog_manager.main_frame.pack(expand=True, fill="both")
        self.blog_manager.load_posts()