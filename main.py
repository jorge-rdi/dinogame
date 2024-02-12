from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dinosaur'

vinculo = MySQL(app)

app.secret_key = 'pepe'


@app.route('/')
def Inicio():
    return render_template('inicio.html')


@app.route('/dinogame')
def Dinogame():
    return render_template('dinogame.html')


@app.route('/gameover', methods=["GET", "POST"])
def GameOver():
    if request.method == 'POST':
        identidad = request.form['nombre']
        cursor = vinculo.connection.cursor()
        cursor.execute("INSERT INTO tabla1 (Nombre) VALUES (%s)", (identidad,))
        vinculo.connection.commit()
        cursor.close()
        return redirect(url_for('obtener'))
    return render_template('gameover.html')


@app.route('/jugadores')
def obtener():
    query = 'SELECT * FROM tabla1'
    cur = vinculo.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return render_template('jugadores.html', data=data)

@app.route('/edit/<id>', methods=['POST', 'GET'])
def get_contact(id):
    # Retrieve employee details based on the provided ID
    cur = vinculo.connection.cursor()
    cur.execute('SELECT * FROM tabla1 WHERE id={0}'.format(id))
    data = cur.fetchall()
    cur.close()

    # Render the 'editindex.html' template with the employee details
    return render_template('editindex.html', contact=data[0])


@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method=='POST':
        name=request.form['nombre']
        cur=vinculo.connection.cursor()
        cur.execute("""
             UPDATE tabla1
             SET Nombre=%s
            WHERE id=%s
        """, (name,id))
        vinculo.connection.commit()
    return redirect(url_for('obtener'))


# Define the route for deleting an employee
@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
    # Execute an SQL DELETE query to remove the employee
    cur = vinculo.connection.cursor()
    cur.execute('DELETE FROM tabla1 WHERE id={0}'.format(id))
    vinculo.connection.commit()

    # Redirect to the index page
    return redirect(url_for('obtener'))

# The remaining routes remain unchanged

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
