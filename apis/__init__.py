from flask_restx import Api

from .posts_namespace import api as nsp

api = Api(
    title='BEKK Endpoints',
    version='1.0',
    description='',
    # All API metadatas
)

api.add_namespace(nsp)