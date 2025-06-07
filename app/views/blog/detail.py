import tkinter as tk
from tkinter import ttk, messagebox
from app.services.blog_service import increment_view_count, add_like, get_post_comments, add_comment
from app.utils.exceptions import BlogError


class BlogDetailView:
    def __init__(self, parent_frame, user, post, blog_viewer):
        self.parent = parent_frame
        self.user = user
        self.post = post
        self.blog_viewer = blog_viewer

        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff", width=700, height=600)
        self.main_frame.pack(fill="both", expand=True)

        # Scrollable text container (no scrollbar)
        self.text = tk.Text(self.main_frame, bg="#f0f8ff", relief="flat", highlightthickness=0, width=80)
        self.text.pack(fill="both", expand=True, padx=25)

        # Embed frame in text
        self.scroll_frame = tk.Frame(self.text, bg="#f0f8ff")
        self.text.window_create("end", window=self.scroll_frame)
        self.scroll_frame.pack(expand=True)

        increment_view_count(post['post_id'])
        self.setup_ui()
        self.load_comments()

    def setup_ui(self):
        container = tk.Frame(self.scroll_frame, bg="#f0f8ff", padx=20, pady=20)
        container.pack(fill="x", expand=True)

        ttk.Button(container, text="← Back", command=self.go_back).pack(anchor="w", pady=(0, 20))

        meta = tk.Frame(container, bg="#f0f8ff")
        meta.pack(fill="x", pady=(0, 15))

        tk.Label(meta, text=self.post['created_at'].strftime("%B %d, %Y"), font=("Helvetica", 10), bg="#f0f8ff", fg="#666").pack(side="left")
        tk.Label(meta, text=f"👁️ {self.post['view_count']} views", font=("Helvetica", 10), bg="#f0f8ff", fg="#666").pack(side="left", padx=20)

        self.likes_label = tk.Label(meta, text=f"❤️ {self.post['like_count']} likes", font=("Helvetica", 10), bg="#f0f8ff", fg="#666", cursor="hand2")
        self.likes_label.pack(side="left")
        self.likes_label.bind("<Button-1>", lambda e: self.handle_like())

        tk.Label(container, text=self.post['title'], font=("Helvetica", 28, "bold"), bg="#f0f8ff", fg="#4b0082", wraplength=800, justify="left").pack(anchor="center", pady=(10, 15))
        tk.Label(container, text=self.post['content'], font=("Helvetica", 12), bg="#f0f8ff", fg="#333", wraplength=800, justify="left").pack(anchor="center", pady=(0, 30))

        # Comments
        tk.Label(container, text="Comments", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#4b0082").pack(anchor="center", pady=(0, 15))
        self.comments_container = tk.Frame(container, bg="#f0f8ff")
        self.comments_container.pack(fill="x", expand=True)

        if self.user:
            self.create_comment_form(container)

    def create_comment_form(self, parent_frame):
        form = tk.Frame(parent_frame, bg="#f0f8ff")
        form.pack(fill="x", pady=(20, 0))
        tk.Label(form, text="Add a comment:", font=("Helvetica", 11, "bold"), bg="#f0f8ff").pack(anchor="w", pady=(0, 5))
        self.comment_text = tk.Text(form, font=("Helvetica", 11), height=3, wrap="word", bg="white", fg="#333", relief="solid", bd=1, padx=5, pady=5)
        self.comment_text.pack(fill="x", pady=(0, 10))
        ttk.Button(form, text="Post Comment", command=self.submit_comment).pack(anchor="e")

    def handle_like(self):
        try:
            add_like(self.post['post_id'], self.user.user_id if self.user else None)
            self.post['like_count'] += 1
            self.likes_label.config(text=f"❤️ {self.post['like_count']} likes")
        except BlogError as e:
            messagebox.showerror("Error", str(e))

    def load_comments(self):
        try:
            for widget in self.comments_container.winfo_children():
                widget.destroy()
            comments = get_post_comments(self.post['post_id'])
            for c in comments:
                self.add_comment_to_ui(c)
        except BlogError as e:
            messagebox.showerror("Error", str(e))

    def add_comment_to_ui(self, comment):
        frame = tk.Frame(self.comments_container, bg="white", bd=1, relief="solid")
        frame.pack(fill="x", pady=5, ipady=5, ipadx=10)

        meta = tk.Frame(frame, bg="white")
        meta.pack(fill="x", anchor="w")
        author = comment.get('author_name') or f"User #{comment['user_id']}" if comment.get('user_id') else "Guest"
        tk.Label(meta, text=author, font=("Helvetica", 10, "bold"), bg="white", fg="#4b0082").pack(side="left")
        tk.Label(meta, text=comment['created_at'].strftime(" • %B %d, %Y %H:%M"), font=("Helvetica", 9), bg="white", fg="#666").pack(side="left", padx=5)

        tk.Label(frame, text=comment['content'], font=("Helvetica", 10), bg="white", fg="#333", wraplength=750, justify="left").pack(anchor="w", pady=(5, 0))

    def submit_comment(self):
        comment = self.comment_text.get("1.0", "end-1c").strip()
        if not comment:
            messagebox.showwarning("Warning", "Enter a comment")
            return
        try:
            new_comment = add_comment(post_id=self.post['post_id'], user_id=self.user.user_id if self.user else None, author_name=None, content=comment)
            self.add_comment_to_ui(new_comment)
            self.comment_text.delete("1.0", "end")
        except BlogError as e:
            messagebox.showerror("Error", str(e))

    def go_back(self):
        self.main_frame.pack_forget()
        self.blog_viewer.main_frame.pack(fill="both", expand=True)
        self.main_frame.destroy()