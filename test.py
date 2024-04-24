from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    # Connect to the SQLite database
    conn = sqlite3.connect('instance/items.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM 'user'")
    rows = cursor.fetchall()
    # Close the database connection
    conn.close()

    # Render the HTML template with the data
    return render_template('indexTEST.html', rows=rows)

# @app.route('/shop')
# def shop():
#     return render_template('')

if __name__ == '__main__':
    app.run(debug=True)
