from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Liste pour stocker les réservations
reservations = []

@app.route('/reserve', methods=['POST'])
def create_reservation():
    data = request.json
    if not all(k in data for k in ("name", "pickup", "destination")):
        return jsonify({"error": "Informations manquantes"}), 400

    # Ajoute une réservation en attente
    reservation = {
        'name': data['name'],
        'pickup': data['pickup'],
        'destination': data['destination'],
        'status': 'en attente'  # Statut initial
    }
    reservations.append(reservation)
    return jsonify({"message": "Réservation ajoutée", "reservation": reservation}), 201

@app.route('/reservations', methods=['GET'])
def get_reservations():
    # Filtre les réservations en attente
    waiting_reservations = [r for r in reservations if r['status'] == 'en attente']
    return jsonify(waiting_reservations), 200

@app.route('/confirm', methods=['POST'])
def confirm_reservation():
    data = request.json
    name = data.get("name")
    pickup = data.get("pickup")
    destination = data.get("destination")

    # Recherche et confirme la réservation
    for reservation in reservations:
        if reservation['name'] == name and reservation['pickup'] == pickup and reservation['destination'] == destination:
            reservation['status'] = 'confirmée'
            return jsonify({"message": "Réservation confirmée"}), 200

    return jsonify({"error": "Réservation non trouvée"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
