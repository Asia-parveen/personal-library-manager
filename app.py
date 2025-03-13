import streamlit as st
import json
import os
import time

# File to store library data
LIBRARY_FILE = "library.json"

# Custom CSS for styling
def set_custom_theme():
    st.markdown(
        """
        <style>
        /* Remove default padding and margin at the top */
        .stApp {
            margin: 0;
            padding: 0;
            background-color: #000000; /* Black background */
            color: #ffffff; /* White text */
        }
        /* Ensure the main content area has no gaps */
        .main .block-container {
            padding-top: 0;
        }
        /* Sidebar styling with dark green background */
        .sidebar .sidebar-content {
            background-color: #006400 !important; /* Dark green */
            padding: 20px !important;
        }
        /* Sidebar text color (black) */
        .sidebar .sidebar-content .stRadio label, 
        .sidebar .sidebar-content .stButton button, 
        .sidebar .sidebar-content .stMarkdown, 
        .sidebar .sidebar-content .stTextInput, 
        .sidebar .sidebar-content .stNumberInput {
            color: #000000 !important; /* Black text */
        }
        /* Increase gap between sidebar options */
        .stRadio > div {
            gap: 30px; /* Larger gap */
        }
        /* Shining white text */
        .st-b7, .st-c0, .st-c1, .stMarkdown, .stTextInput, .stNumberInput, .stRadio, .stButton {
            color: #ffffff !important;
            text-shadow: 0 0 5px #ffffff, 0 0 10px #ffffff, 0 0 20px #ffffff;
        }
        /* Button styling */
        .stButton button {
            background-color: #00bfff !important; /* Blue */
            color: #ffffff !important;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
        }
        .stButton button:hover {
            background-color: #ffcc00 !important; /* Yellow */
            color: #000000 !important;
        }
        /* Custom radio buttons (blue) */
        .stRadio > label {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 16px;
            color: #00bfff !important; /* Blue text */
        }
        /* Animation for success/error messages */
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .stAlert {
            animation: fadeIn 1s ease-in-out;
        }
        /* Bullet points styling */
        .stMarkdown ul li {
            color: #ffcc00; /* Yellow */
            font-size: 16px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file)

# Add a book
def add_book(library):
    st.subheader("📖 Add a Book", anchor=False)
    st.write("Enter the details of the book you want to add to your library.")
    title = st.text_input("📘 Title", key="title")
    author = st.text_input("🖋️ Author", key="author")
    year = st.number_input("📅 Publication Year", min_value=1000, max_value=9999, step=1, key="year")
    genre = st.text_input("📚 Genre", key="genre")
    read_status = st.radio("📖 Have you read this book?", ("Yes", "No"), key="read_status")
    
    if st.button("➕ Add Book", key="add_book"):
        if title and author and year and genre:
            book = {
                "title": title,
                "author": author,
                "year": int(year),
                "genre": genre,
                "read_status": read_status == "Yes"
            }
            library.append(book)
            save_library(library)
            st.success(f"✅ Book '{title}' added successfully!")
            time.sleep(1)  # Animation delay
            st.balloons()  # Celebration animation

            # Display added book details
            st.subheader("📄 Book Details", anchor=False)
            st.markdown(
                f"""
                - 📖 **Title:** {book['title']}
                - 🖋️ **Author:** {book['author']}
                - 📅 **Year:** {book['year']}
                - 📚 **Genre:** {book['genre']}
                - 📖 **Status:** {'✅ Read' if book['read_status'] else '❌ Unread'}
                """
            )
        else:
            st.error("❌ Please fill in all fields.")

# Remove a book
def remove_book(library):
    st.subheader("🗑️ Remove a Book", anchor=False)
    st.write("Enter the title of the book you want to remove from your library.")
    title_to_remove = st.text_input("📘 Enter the title of the book to remove", key="remove_title")
    
    if st.button("➖ Remove Book", key="remove_book"):
        initial_count = len(library)
        library[:] = [book for book in library if book["title"].lower() != title_to_remove.lower()]
        if len(library) < initial_count:
            save_library(library)
            st.success(f"✅ Book '{title_to_remove}' removed successfully!")
            time.sleep(1)  # Animation delay
        else:
            st.error(f"❌ Book '{title_to_remove}' not found.")

# Search for a book
def search_book(library):
    st.subheader("🔍 Search for a Book", anchor=False)
    st.write("Search for a book in your library by title or author.")
    search_by = st.radio("🔎 Search by:", ("Title", "Author"), key="search_by")
    search_term = st.text_input(f"🔍 Enter the {search_by.lower()}", key="search_term")
    
    if st.button("🔍 Search", key="search_button"):
        matching_books = []
        for book in library:
            if search_by == "Title" and search_term.lower() in book["title"].lower():
                matching_books.append(book)
            elif search_by == "Author" and search_term.lower() in book["author"].lower():
                matching_books.append(book)
        
        if matching_books:
            st.write("📚 Matching Books:")
            for i, book in enumerate(matching_books, 1):
                st.markdown(
                    f"""
                    - 📖 **Title:** {book['title']}
                    - 🖋️ **Author:** {book['author']}
                    - 📅 **Year:** {book['year']}
                    - 📚 **Genre:** {book['genre']}
                    - 📖 **Status:** {'✅ Read' if book['read_status'] else '❌ Unread'}
                    """
                )
        else:
            st.write("❌ No matching books found.")

# Display all books
def display_all_books(library):
    st.subheader("📚 Your Library", anchor=False)
    st.write("Here is a list of all the books in your library.")
    if library:
        for i, book in enumerate(library, 1):
            st.markdown(
                f"""
                - 📖 **Title:** {book['title']}
                - 🖋️ **Author:** {book['author']}
                - 📅 **Year:** {book['year']}
                - 📚 **Genre:** {book['genre']}
                - 📖 **Status:** {'✅ Read' if book['read_status'] else '❌ Unread'}
                """
            )
    else:
        st.write("📭 Your library is empty.")

# Display statistics
def display_statistics(library):
    st.subheader("📊 Library Statistics", anchor=False)
    st.write("Here are some statistics about your library.")
    total_books = len(library)
    read_books = sum(book["read_status"] for book in library)
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
    st.write(f"📚 **Total books:** {total_books}")
    st.write(f"📖 **Percentage read:** {percentage_read:.1f}%")

# Main function
def main():
    # Set custom theme
    set_custom_theme()
    
    # Application Description
    st.title("📚 Personal Library Manager")
    st.subheader("📌 Organize Your Books Easily")
    st.write(
        """
        Welcome to the **Personal Library Manager**! This application helps you manage your book collection efficiently. 
        You can add, remove, search, and view all your books in one place. Additionally, you can track your reading 
        progress with statistics like the total number of books and the percentage of books you've read.
        """
    )
    
    # Sidebar with icons and text
    st.sidebar.markdown('<h1 style="color:black;">📖 Menu</h1>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="color:black;">Select an option from the menu to manage your library.</p>', unsafe_allow_html=True)

    
    # Load library
    library = load_library()
    
    # Menu options with icons and gaps
    menu_options = {
        "📖 Add a Book": add_book,
        "🗑️ Remove a Book": remove_book,
        "🔍 Search for a Book": search_book,
        "📚 Display All Books": display_all_books,
        "📊 Display Statistics": display_statistics
    }
    
    # Sidebar with icons and emojis
    choice = st.sidebar.radio("Select an option", list(menu_options.keys()))
    
    # Execute selected option
    menu_options[choice](library)
    
    # Exit and save
    if st.sidebar.button("🚪 Exit"):
        save_library(library)
        st.sidebar.write("📁 Library saved to file. Goodbye! 👋")
        st.stop()

# Run the app
if __name__ == "__main__":
    main()


# import streamlit as st
# import json
# import os
# import time

# # File to store library data
# LIBRARY_FILE = "library.json"

# # Custom CSS for black theme, animations, and styling
# def set_custom_theme():
#     st.markdown(
#         """
#         <style>
#         /* Black theme starting from the top */
#         body, .stApp {
#             background-color: #000000;
#             color: #ffffff;
#         }
#         /* Sidebar styling with gaps */
#         .css-1d391kg {
#             background-color: #1a1a1a !important;
#             padding: 20px !important;
#         }
#         .stRadio > div {
#             gap: 20px; /* Add gap between sidebar options */
#         }
#         /* Shining white text */
#         .st-b7, .st-c0, .st-c1, .stMarkdown, .stTextInput, .stNumberInput, .stRadio, .stButton {
#             color: #ffffff !important;
#             text-shadow: 0 0 5px #ffffff, 0 0 10px #ffffff, 0 0 20px #ffffff;
#         }
#         /* Button styling */
#         .stButton button {
#             background-color: #00bfff !important; /* Blue */
#             color: #ffffff !important;
#             border-radius: 10px;
#             padding: 10px 20px;
#             font-weight: bold;
#         }
#         .stButton button:hover {
#             background-color: #ffcc00 !important; /* Yellow */
#             color: #000000 !important;
#         }
#         /* Animation for success/error messages */
#         @keyframes fadeIn {
#             0% { opacity: 0; }
#             100% { opacity: 1; }
#         }
#         .stAlert {
#             animation: fadeIn 1s ease-in-out;
#         }
#         /* Bullet points styling */
#         .stMarkdown ul li {
#             color: #ffcc00; /* Yellow */
#             font-size: 16px;
#             margin-bottom: 10px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

# # Load library from file
# def load_library():
#     if os.path.exists(LIBRARY_FILE):
#         with open(LIBRARY_FILE, "r") as file:
#             return json.load(file)
#     return []

# # Save library to file
# def save_library(library):
#     with open(LIBRARY_FILE, "w") as file:
#         json.dump(library, file)

# # Add a book
# def add_book(library):
#     st.subheader("📖 Add a Book", anchor=False)
#     title = st.text_input("📘 Title", key="title")
#     author = st.text_input("🖋️ Author", key="author")
#     year = st.number_input("📅 Publication Year", min_value=1000, max_value=9999, step=1, key="year")
#     genre = st.text_input("📚 Genre", key="genre")
#     read_status = st.radio("📖 Have you read this book?", ("Yes", "No"), key="read_status")
    
#     if st.button("➕ Add Book", key="add_book"):
#         if title and author and year and genre:
#             book = {
#                 "title": title,
#                 "author": author,
#                 "year": int(year),
#                 "genre": genre,
#                 "read_status": read_status == "Yes"
#             }
#             library.append(book)
#             save_library(library)
#             st.success(f"✅ Book '{title}' added successfully!")
#             time.sleep(1)  # Animation delay
#             st.balloons()  # Celebration animation
#         else:
#             st.error("❌ Please fill in all fields.")

# # Remove a book
# def remove_book(library):
#     st.subheader("🗑️ Remove a Book", anchor=False)
#     title_to_remove = st.text_input("📘 Enter the title of the book to remove", key="remove_title")
    
#     if st.button("➖ Remove Book", key="remove_book"):
#         initial_count = len(library)
#         library[:] = [book for book in library if book["title"].lower() != title_to_remove.lower()]
#         if len(library) < initial_count:
#             save_library(library)
#             st.success(f"✅ Book '{title_to_remove}' removed successfully!")
#             time.sleep(1)  # Animation delay
#         else:
#             st.error(f"❌ Book '{title_to_remove}' not found.")

# # Search for a book
# def search_book(library):
#     st.subheader("🔍 Search for a Book", anchor=False)
#     search_by = st.radio("🔎 Search by:", ("Title", "Author"), key="search_by")
#     search_term = st.text_input(f"🔍 Enter the {search_by.lower()}", key="search_term")
    
#     if st.button("🔍 Search", key="search_button"):
#         matching_books = []
#         for book in library:
#             if search_by == "Title" and search_term.lower() in book["title"].lower():
#                 matching_books.append(book)
#             elif search_by == "Author" and search_term.lower() in book["author"].lower():
#                 matching_books.append(book)
        
#         if matching_books:
#             st.write("📚 Matching Books:")
#             for i, book in enumerate(matching_books, 1):
#                 st.markdown(
#                     f"""
#                     - 📖 **Title:** {book['title']}
#                     - 🖋️ **Author:** {book['author']}
#                     - 📅 **Year:** {book['year']}
#                     - 📚 **Genre:** {book['genre']}
#                     - 📖 **Status:** {'✅ Read' if book['read_status'] else '❌ Unread'}
#                     """
#                 )
#         else:
#             st.write("❌ No matching books found.")

# # Display all books
# def display_all_books(library):
#     st.subheader("📚 Your Library", anchor=False)
#     if library:
#         for i, book in enumerate(library, 1):
#             st.markdown(
#                 f"""
#                 - 📖 **Title:** {book['title']}
#                 - 🖋️ **Author:** {book['author']}
#                 - 📅 **Year:** {book['year']}
#                 - 📚 **Genre:** {book['genre']}
#                 - 📖 **Status:** {'✅ Read' if book['read_status'] else '❌ Unread'}
#                 """
#             )
#     else:
#         st.write("📭 Your library is empty.")

# # Display statistics
# def display_statistics(library):
#     st.subheader("📊 Library Statistics", anchor=False)
#     total_books = len(library)
#     read_books = sum(book["read_status"] for book in library)
#     percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    
#     st.write(f"📚 **Total books:** {total_books}")
#     st.write(f"📖 **Percentage read:** {percentage_read:.1f}%")

# # Main function
# def main():
#     # Set custom theme
#     set_custom_theme()
    
#     st.title("📚 Personal Library Manager")
#     st.sidebar.title("📖 Menu")
    
#     # Load library
#     library = load_library()
    
#     # Menu options with icons and gaps
#     menu_options = {
#         "📖 Add a Book": add_book,
#         "🗑️ Remove a Book": remove_book,
#         "🔍 Search for a Book": search_book,
#         "📚 Display All Books": display_all_books,
#         "📊 Display Statistics": display_statistics
#     }
    
#     # Sidebar with icons and emojis
#     choice = st.sidebar.radio("Select an option", list(menu_options.keys()))
    
#     # Execute selected option
#     menu_options[choice](library)
    
#     # Exit and save
#     if st.sidebar.button("🚪 Exit"):
#         save_library(library)
#         st.sidebar.write("📁 Library saved to file. Goodbye! 👋")
#         st.stop()

# # Run the app
# if __name__ == "__main__":
#     main()



