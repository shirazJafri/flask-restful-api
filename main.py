from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Wrap our app in an API.
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class VideoModel(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String(100), nullable= False)
    views = db.Column(db.Integer, nullable= False)
    likes = db.Column(db.Integer, nullable= False)

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

# Getting on with our YouTube example.

# This object is instantiated to provide a sort of guideline as to what the argument of a video would look like.
video_put_args = reqparse.RequestParser()
# The help argument specifies the message visible to the client if a required argument is missing, is set to None otherwise.
video_put_args.add_argument("name", type= str, help="Name of the video missing!", required= True)
video_put_args.add_argument("likes", type= int, help="Likes on the video missing!", required= True)
video_put_args.add_argument("views", type= int, help="Views of the video missing!", required= True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type= str, help="Name of the video missing!")
video_update_args.add_argument("likes", type= int, help="Likes on the video missing!")
video_update_args.add_argument("views", type= int, help="Views of the video missing!")

# This is used as a serving to the decorator to describe the form the serialization needs to take as the response output.
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Declaring a class that inherits from Resource which let's us override the methods provided by Resource such as handling
# GET, PUT, etc. requests.
class Video(Resource):

    # GET method to return a video based on it's id.
    # This here is a decorator that takes the output of the function (which is an instance of the model)
    # and seralizes it according to the resource fields described above.
    @marshal_with(resource_fields)
    def get(self, video_id):
        # abort_if_video_id_doesnt_exist(video_id= video_id)
        # return videos[video_id]
        result = VideoModel.query.filter_by(id=video_id).first()

        if not result:
            abort(404, message="Could not find video with that ID.")

        return result

    # Access the arguments passed in a request.
    @marshal_with(resource_fields)
    def put(self, video_id):
        # The incoming data is of form type, hence needs to be parsed for use.
        args = video_put_args.parse_args()

        # Checking to see if a video with the id specified as a parameter already exists.
        result = VideoModel.query.filter_by(id=video_id).first()

        if result:
            abort(409, message= "Video ID taken...")

        # Instantiating and subsequently committing the changes to DB.
        video = VideoModel(id=video_id, name= args['name'], views= args['views'], likes= args['likes'])

        db.session.add(video)
        db.session.commit()

        return video, 201 # --> Status Code for successful creation.

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()

        result= VideoModel.query.filter_by(id= video_id).first()

        if not result:
            abort(404, message="The video does not exist!")

        if args['name']:
            result.name= args['name']
        
        if args['views']:
            result.views= args['views']

        if args['likes']:
            result.likes= args['likes']

        db.session.commit()

        return result, 204 # --> Status Code for successful update


    def delete(self, video_id):

        result = VideoModel.query.filter_by(id= video_id).first()

        if not result:
            abort(404, message="Video with this ID does not exist!")

        db.session.delete(result)

        db.session.commit()
        
        # del videos[video_id]
        return '', 204 # --> Status Code for successful deletion.

# Registers a resource that helps map a relevant request on endpoint.
api.add_resource(Video, '/video/<int:video_id>')


if __name__== "__main__":
    # Starts our server/Flask Application.
    app.run(debug=True)