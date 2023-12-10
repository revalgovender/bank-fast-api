from bank.app import create_app, create_db
import uvicorn

app = create_app()

create_db()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8899)
