import tkinter as tk
from tkinter import ttk, messagebox
from app.services.blog_service import get_all_published_posts, get_post_comments
from app.utils.exceptions import BlogError


class BlogViewer:
    def __init__(self, parent_frame, user):
        self.parent = parent_frame
        self.user = user

        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff", width=800)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Blog Posts",
            font=("Helvetica", 24, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        ).pack(anchor="center", padx=20, pady=10)

        # Scrollable Text widget used as a container (no scrollbar)
        self.text = tk.Text(self.main_frame, bg="#f0f8ff", relief="flat", highlightthickness=0, width=80)
        self.text.pack(fill="both", expand=True, padx=25)

        # Embedding a frame inside the Text widget
        self.scroll_frame = tk.Frame(self.text, bg="#f0f8ff")
        self.text.window_create("end", window=self.scroll_frame)
        self.scroll_frame.pack(expand=True)

        self.load_blog_posts()

    def load_blog_posts(self):
        try:
            posts = get_all_published_posts()
            if not posts:
                tk.Label(self.scroll_frame, text="No blog posts yet.", bg="#f0f8ff").pack()
                return

            for post in posts:
                comments = get_post_comments(post['post_id'])
                self.create_post_card(post, len(comments))

        except BlogError as e:
            messagebox.showerror("Error", str(e))

    def create_post_card(self, post, comment_count):
        card = tk.Frame(self.scroll_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", expand=True, padx=20, pady=6)

        # Layout inside card
        content = tk.Frame(card, bg="white")
        content.pack(fill="x", expand=True, padx=20, pady=10)

        tk.Label(content, text="📝", font=("Helvetica", 36), bg="white", width=4).pack(side="left", padx=(0, 10))

        body = tk.Frame(content, bg="white")
        body.pack(fill="x", expand=True)

        tk.Label(body, text=post['created_at'].strftime("%B %d, %Y"), font=("Helvetica", 9), bg="white", fg="#666").pack(anchor="w")
        tk.Label(body, text=post['title'], font=("Helvetica", 16, "bold"), bg="white", fg="#4b0082").pack(anchor="w", pady=4)
        tk.Label(body, text=post['excerpt'], font=("Helvetica", 11), bg="white", fg="#333333", wraplength=700, justify="left").pack(anchor="w", pady=4)

        stats = tk.Frame(body, bg="white")
        stats.pack(anchor="w", pady=(4, 0))

        for txt in [f"👁️ {post['view_count']}", f"❤️ {post['like_count']}", f"💬 {comment_count}"]:
            tk.Label(stats, text=txt, font=("Helvetica", 10), bg="white", fg="#666").pack(side="left", padx=(0, 15))

        # Make full card clickable
        for widget in [card, content, body, stats]:
            widget.bind("<Button-1>", lambda e, p=post: self.show_post_detail(p))
            for child in widget.winfo_children():
                child.bind("<Button-1>", lambda e, p=post: self.show_post_detail(p))

    def show_post_detail(self, post):
        self.main_frame.pack_forget()
        from .detail import BlogDetailView
        BlogDetailView(self.parent, self.user, post, self)