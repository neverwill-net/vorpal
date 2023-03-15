from flask import jsonify, send_file, request
from media.database import get_session
from media.models import MediaFile
from app import app
from flask import jsonify

@app.route('/', methods=['GET'])
def index():
    routes = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':  # Exclude static files route
            routes[rule.endpoint] = {
                'url': str(rule),
                'methods': list(rule.methods),
            }
    return jsonify(routes)

@app.route('/api/media', methods=['GET'])
def get_all_media():
    session = get_session()
    media_files = session.query(MediaFile).all()
    return jsonify([media_file.to_dict() for media_file in media_files])

@app.route('/api/media/search', methods=['GET'])
def search_media():
    session = get_session()
    query = session.query(MediaFile)
    args = request.args

    for attr in args:
        if hasattr(MediaFile, attr):
            query = query.filter(getattr(MediaFile, attr).ilike(f"%{args[attr]}%"))

    media_files = query.all()
    return jsonify([media_file.to_dict() for media_file in media_files])

@app.route('/api/media', methods=['POST'])
def add_media():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request data"}), 400

    # Add code to process the uploaded media file and extract metadata

    session = get_session()
    session.add(new_media)
    session.commit()

    return jsonify(new_media.to_dict()), 201

@app.route('/api/media/<string:media_id>', methods=['PUT'])
def update_media(media_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request data"}), 400

    session = get_session()
    media_file = session.query(MediaFile).filter(MediaFile.unique_id == media_id).one_or_none()

    if media_file:
        for key, value in data.items():
            if hasattr(media_file, key):
                setattr(media_file, key, value)

        session.commit()
        return jsonify(media_file.to_dict())
    else:
        return jsonify({"error": "Media file not found"}), 404

@app.route('/api/media/<string:media_id>', methods=['DELETE'])
def delete_media(media_id):
    session = get_session()
    media_file = session.query(MediaFile).filter(MediaFile.unique_id == media_id).one_or_none()

    if media_file:
        session.delete(media_file)
        session.commit()
        return jsonify({"result": "Media file deleted"})
    else:
        return jsonify({"error": "Media file not found"}), 404

@app.route('/api/media/<string:media_id>', methods=['GET'])
def get_media(media_id):
    if not media_id:
        return jsonify({"error": "Invalid media ID"}), 400

    session = get_session()
    media_file = session.query(MediaFile).filter(MediaFile.unique_id == media_id).one_or_none()
    if media_file:
        return jsonify(media_file.to_dict())
    else:
        return jsonify({"error": "Media file not found"}), 404

@app.route('/api/stream/<string:media_id>', methods=['GET'])
def stream_media(media_id):
    if not media_id:
        return jsonify({"error": "Invalid media ID"}), 400

    session = get_session()
    media_file = session.query(MediaFile).filter(MediaFile.unique_id == media_id).one_or_none()
    if media_file:
        #return send_file(media_file.file_path, as_attachment=True, attachment_filename=media_file.file_name)
        return send_file(media_file.file_path, mimetype=media_file.format_long_name)
    else:
        return jsonify({"error": "Media file not found"}), 404

@app.route('/api/media/format/<string:format_name>', methods=['GET'])
def get_media_by_format(format_name):
    if not format_name:
        return jsonify({"error": "Invalid format name"}), 400

    session = get_session()
    media_files = session.query(MediaFile).filter(MediaFile.format_name == format_name).all()
    return jsonify([media_file.to_dict() for media_file in media_files])

@app.route('/api/media/metadata/<string:metadata_key>/<string:metadata_value>', methods=['GET'])
def get_media_by_metadata(metadata_key, metadata_value):
    if not metadata_key or not metadata_value:
        return jsonify({"error": "Invalid metadata key or value"}), 400

    session = get_session()
    media_files = session.query(MediaFile).filter(MediaFile.media_metadata[metadata_key].astext == metadata_value).all()
    return jsonify([media_file.to_dict() for media_file in media_files])

@app.route('/api/media/<string:media_id>/metadata', methods=['GET'])
def get_media_metadata(media_id):
    if not media_id:
        return jsonify({"error": "Invalid media ID"}), 400

    session = get_session()
    media_file = session.query(MediaFile).filter(MediaFile.unique_id == media_id).one_or_none()
    
    if media_file:
        return jsonify(media_file.media_metadata)
    else:
        return jsonify({"error": "Media file not found"}), 404


