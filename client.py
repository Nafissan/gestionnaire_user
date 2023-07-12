import requests
import json

# URL du service web
base_url = 'http://localhost:5000'

# Fonction pour effectuer une requête POST
def post_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response.json()

# Fonction pour effectuer une requête PUT
def put_request(url, data):
    headers = {'Content-Type': 'application/json'}
    response = requests.put(url, data=json.dumps(data), headers=headers)
    return response.json()

# Fonction pour effectuer une requête DELETE
def delete_request(url):
    response = requests.delete(url)
    return response.json()

# Fonction pour effectuer une requête GET
def get_request(url):
    response = requests.get(url)
    return response.json()

# Test d'authentification
def test_authentification():
    url = base_url + '/authentification'
    data = {
        'username': 'admin',
        'password': 'passer'
    }
    response = post_request(url, data)
    print(response['message'])

# Test d'ajout d'un utilisateur
def test_ajouter_utilisateur():
    url = base_url + '/utilisateurs'
    data = {
        'username': 'alice',
        'password': 'password456'
    }
    response = post_request(url, data)
    print(response['message'])

# Test de modification d'un utilisateur
def test_modifier_utilisateur(user_id):
    url = base_url + '/utilisateurs/' + str(user_id)
    data = {
        'username' : 'alice',
        'password': 'newpassword789'
    }
    response = put_request(url, data)
    print(response['message'])

# Test de suppression d'un utilisateur
def test_supprimer_utilisateur(user_id):
    url = base_url + '/utilisateurs/' + str(user_id)
    response = delete_request(url)
    print(response['message'])

# Test de listage des utilisateurs
def test_lister_utilisateurs():
    url = base_url + '/utilisateurs'
    response = get_request(url)
    utilisateurs = response
    for utilisateur in utilisateurs:
        print("ID:", utilisateur['id'])
        print("Nom d'utilisateur:", utilisateur['username'])
        print("Mot de passe:", utilisateur['password'])
        print("---------------------------")

# Exécution des tests
test_authentification()
test_ajouter_utilisateur()
test_lister_utilisateurs()
test_modifier_utilisateur(1)  # Modifier l'utilisateur avec l'ID 1
test_supprimer_utilisateur(2)  # Supprimer l'utilisateur avec l'ID 2
test_lister_utilisateurs()
