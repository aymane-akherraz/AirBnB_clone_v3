#!/usr/bin/python3
""" Place_reviews module: This module defines the API routes
for handling reviews in the Flask app.
It includes route handlers for retrieving all reviews for a place,
retrieving a specific review by ID, deleting a review, creating a new review,
and updating an existing review.

Routes:
- GET /places/<place_id>/reviews: Retrieve all reviews for a place.
- GET /reviews/<review_id>: Retrieve a specific review by ID.
- DELETE /reviews/<review_id>: Delete a review.
- POST /places/<place_id>/reviews: Create a new review for a place.
- PUT /reviews/<review_id>: Update an existing review.
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_of_place(place_id):
    """ Retrieves the list of all Review objects of a place """
    place = storage.get("Place", place_id)
    if place:
        return jsonify([review.to_dict() for review in place.reviews])
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """ Retrieve a Review object """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if review:
        review.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def insert_new_review(place_id):
    """ Creates a Review object """
    if storage.get("Place", place_id):
        review = request.get_json(silent=True)
        if review is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in review:
            abort(400, 'Missing user_id')
        if storage.get("User", review['user_id']) is None:
            abort(404)
        if 'text' not in review:
            abort(400, 'Missing text')
        my_dict = {**review, 'place_id': place_id}
        new = Review(**my_dict)
        new.save()
        return jsonify(new.to_dict()), 201
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            if k not in ["id", "user_id", "place_id", "created_at",
                         "updated_at"]:
                setattr(review, k, v)
        review.save()
        return jsonify(review.to_dict())
    abort(404)
