from flask import Flask, request, jsonify
import mysql.connector
import hashlib

app = Flask(__name__)

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="mglsi_user",
    password="passer",
    database="mglsi_news"
)

# Route pour l'authentification
@app.route('/authentification', methods=['POST'])
def authentification():
    data = request.get_json()
    username = data['username']
    password = hashlib.md5(data['password'].encode()).hexdigest()


    # Vérification des informations d'authentification dans la base de données
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE login = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({'message': 'Authentification réussie'})
    else:
        return jsonify({'message': 'Échec de l\'authentification'})

# Route pour l'ajout d'un utilisateur
@app.route('/utilisateurs', methods=['POST'])
def ajouter_utilisateur():
    data = request.get_json()
    username = data['username']
    password = hashlib.md5(data['password'].encode()).hexdigest()
    # Ajout de l'utilisateur dans la base de données
    cursor = db.cursor()
    cursor.execute("INSERT INTO utilisateur (login, password) VALUES (%s, %s)", (username, password))
    db.commit()
    cursor.close()

    return jsonify({'message': 'Utilisateur ajouté avec succès'})

# Route pour la modification d'un utilisateur
@app.route('/utilisateurs/<int:user_id>', methods=['PUT'])
def modifier_utilisateur(user_id):
    data = request.get_json()
    new_password = hashlib.md5(data['password'].encode()).hexdigest()
    new_username = data['username']

    # Modification du mot de passe de l'utilisateur dans la base de données
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'})
    else:
        cursor = db.cursor()
        cursor.execute("UPDATE utilisateur SET login= %s ,password = %s WHERE id = %s", (new_username,new_password, user_id))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Utilisateur modifié avec succès'})

      
# Route pour la suppression d'un utilisateur
@app.route('/utilisateurs/<int:user_id>', methods=['DELETE'])
def supprimer_utilisateur(user_id):
    # Suppression de l'utilisateur de la base de données
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'})
    else :
        cursor = db.cursor()
        cursor.execute("DELETE FROM utilisateur WHERE id = %s", (user_id,))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Utilisateur supprimé avec succès'})

# Route pour lister tous les utilisateurs
@app.route('/utilisateurs', methods=['GET'])
def lister_utilisateurs():
    # Récupération de tous les utilisateurs de la base de données
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateur")
    utilisateurs = cursor.fetchall()
    cursor.close()

    # Formatage des utilisateurs en une liste de dictionnaires
    result = []
    for utilisateur in utilisateurs:
        user_dict = {
            'id': utilisateur[0],
            'username': utilisateur[1],
            'password': utilisateur[2]
        }
        result.append(user_dict)

    return jsonify(result)

if __name__ == '__main__':
    app.run()
