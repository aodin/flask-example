"""
An example script that uses the app models.
"""
from pathlib import Path
import sys

root = Path(__file__).absolute().parent.parent
sys.path.insert(0, str(root))

from app import create_app
from app.users import User


def main():
    app = create_app()
    with app.app_context():
        users = User.query.all()
        print(users)


if __name__ == '__main__':
    main()
