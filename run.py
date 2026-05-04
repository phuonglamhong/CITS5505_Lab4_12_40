from dotenv import load_dotenv
from final_project import create_app, db
load_dotenv()
app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created.")

if __name__ == "__main__":
    app.run(debug=True)