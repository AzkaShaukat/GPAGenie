import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from app.services.blog_service import (
    get_all_posts,
    delete_post,
    create_post,
    update_post
)
from app.utils.exceptions import BlogError
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
IMAGE_DIR = os.path.join(PROJECT_ROOT, "app", "static", "blog_images")

class BlogManager:
    def __init__(self, parent_frame, user):
        self.parent = parent_frame
        self.user = user
        self.post_images = {}

        self.main_frame = tk.Frame(parent_frame, bg="#f0f8ff", width=800)
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(
            self.main_frame,
            text="Manage Blog Posts",
            font=("Helvetica", 24, "bold"),
            bg="#f0f8ff",
            fg="#4b0082"
        ).pack(anchor="center", padx=20, pady=10)

        # Scrollable Text widget used as a container (no external scrollbar)
        self.text = tk.Text(self.main_frame, bg="#f0f8ff", relief="flat", highlightthickness=0, width=80)
        self.text.pack(fill="both", expand=True, padx=25)

        # Embedding a frame inside the Text widget
        self.posts_frame = tk.Frame(self.text, bg="#f0f8ff")
        self.text.window_create("end", window=self.posts_frame)
        self.posts_frame.pack(expand=True)

        self.load_posts()

        # Add "New Post" button at the bottom
        self.add_post_btn = ttk.Button(
            self.main_frame,
            text="+ Add New Blog Post",
            command=self.show_add_post_form,
            style="Accent.TButton",
            width=20
        )
        self.add_post_btn.pack(pady=20)

    def load_posts(self):
        """Load all blog posts from database"""
        try:
            # Clear existing posts
            for widget in self.posts_frame.winfo_children():
                widget.destroy()

            posts = get_all_posts()
            if not posts:
                tk.Label(
                    self.posts_frame,
                    text="No blog posts yet. Click 'Add New' to create one.",
                    font=("Helvetica", 12),
                    bg="#f0f8ff"
                ).pack(pady=50)
                return

            for post in posts:
                self.create_post_card(post)

        except BlogError as e:
            messagebox.showerror("Error", f"Failed to load posts: {str(e)}")

    def create_post_card(self, post):
        """Create a card for each blog post with edit/delete buttons"""
        card = tk.Frame(self.posts_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", expand=True, padx=20, pady=6)

        # Left column for icon
        icon_frame = tk.Frame(card, bg="white")
        icon_frame.pack(side="left", padx=10)
        tk.Label(
            icon_frame,
            text="📝",
            font=("Helvetica", 36),
            bg="white",
            width=4
        ).pack(side="left", padx=(0, 10))

        # Main content frame
        content_frame = tk.Frame(card, bg="white")
        content_frame.pack(side="left", fill="both", expand=True, padx=10)

        # Post content
        tk.Label(
            content_frame,
            text=post['created_at'].strftime("%B %d, %Y"),
            font=("Helvetica", 9),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        tk.Label(
            content_frame,
            text=post['title'],
            font=("Helvetica", 16, "bold"),
            bg="white",
            fg="#4b0082",
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=5)

        tk.Label(
            content_frame,
            text=post['excerpt'],
            font=("Helvetica", 11),
            bg="white",
            fg="#333333",
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=(0, 10))

        # Stats
        stats_frame = tk.Frame(content_frame, bg="white")
        stats_frame.pack(anchor="w")

        tk.Label(
            stats_frame,
            text=f"👁️ {post['view_count']}",
            font=("Helvetica", 10),
            bg="white",
            fg="#666666"
        ).pack(side="left", padx=(0, 15))

        tk.Label(
            stats_frame,
            text=f"❤️ {post['like_count']}",
            font=("Helvetica", 10),
            bg="white",
            fg="#666666"
        ).pack(side="left", padx=(0, 15))

        # Right column for buttons
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(side="right", padx=10)

        ttk.Button(
            btn_frame,
            text="Update",
            command=lambda p=post: self.show_edit_form(p),
            width=8
        ).pack(side="top", pady=2)

        ttk.Button(
            btn_frame,
            text="Delete",
            command=lambda p=post: self.confirm_delete(p),
            style="Danger.TButton",
            width=8
        ).pack(side="top", pady=2)

    def confirm_delete(self, post):
        """Show confirmation dialog before deleting"""
        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{post['title']}'?\nThis cannot be undone."
        ):
            try:
                delete_post(post['post_id'])
                messagebox.showinfo("Success", "Post deleted successfully")
                self.load_posts()  # Refresh the list
            except BlogError as e:
                messagebox.showerror("Error", f"Failed to delete post: {str(e)}")

    def show_add_post_form(self):
        """Show form to add new blog post"""
        from .post_form import BlogPostForm
        self.main_frame.pack_forget()

        # Ensure user_id is available
        if not hasattr(self.user, 'user_id'):
            messagebox.showerror("Error", "User ID is missing. Please log in or contact support.")
            return

        BlogPostForm(self.parent, self.user, self, mode="create")

    def show_edit_form(self, post):
        """Show form to edit existing blog post"""
        from .post_form import BlogPostForm
        self.main_frame.pack_forget()
        BlogPostForm(self.parent, self.user, self, mode="edit", post=post)