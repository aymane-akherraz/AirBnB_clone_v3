#!/usr/bin/python3
""" reviews module """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_of_place(place_id):
    """ Retrieves the list of all Review objects of a place """

    place = storage.get(Place, place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id=None):
    """ Retrieve a Review object """

    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def remove_review(review_id):
    """ Deletes a Review object """

    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def insert_new_review(place_id):
    """ Creates a Review object """

    if storage.get(Place, place_id):
        review = request.get_json()
        if review is not None:
            if 'user_id' not in review:
                abort(400, 'Missing user_id')
            if storage.get(User, review['user_id']) is None:
                abort(404)
            if 'text' not in review:
                abort(400, 'Missing text')
            new = review(**review, place_id=place_id)
            new.save()
            return jsonify(new.to_dict()), 201
        abort(400, 'Not a JSON')
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """ Updates a Review object """

    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if data is not None:
            for k, v in data.items():
                if k not in ["id", "user_id", "place_id", "created_at",
                             "updated_at"]:
                    setattr(review, k, v)
            review.save()
            return jsonify(review.to_dict())
        abort(400, 'Not a JSON')
    abort(404)
