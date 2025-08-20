# Mini Inventory — Simple+

Clean, simple inventory app with categories, images, search, and pagination.

## Features
- CRUD for items (name, SKU, category, quantity, price, image)
- Search by name/SKU and filter by category
- Pagination (8 per page)
- Summary: total quantity & total value
- Simple category manager
- Login required (Django auth)
- SQLite database

## Quickstart
```bash
cd mini_inventory_simple_plus
python -m venv env
# Windows: env\Scripts\activate
# macOS/Linux: source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Then open http://127.0.0.1:8000/

## Notes
- File uploads go to the `media/items/` folder.
- Use the **Categories** page to add categories before creating items (optional).
