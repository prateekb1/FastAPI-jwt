import uvicorn
from fastapi import FastAPI
from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
# from app.auth.jwt_bearer import JWTBearer

posts =  [
    {
        "id" : 1,
        "title" : "penguins",
        "text" : "some text about penguins"
    },
    {
        "id" : 2,
        "title" : "Tigers",
        "text" : "tigers are largest living cat species"
    },
    {
        "id" : 3,
        "title" : "Koalas",
        "text" : "some text about Koalas"
    }
]

users = []

app = FastAPI()

# Get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}

# Get Posts
@app.get("/posts", tags=["posts"])
def get_posts():
    return {"data": posts}


# Get single post {id}
@app.get("/posts/{id}", tags=["posts"])
def get_one_post(id : int):
    if id > len(posts):
        return {
            "error":"Post with this ID does not exist"
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data":post
            }
        
# 4 Post a blog post [A handler for creating a post]
@app.post("/posts", tags=["posts"])
def add_post(post : PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "info": "Post Added!"
    }

# 5 User Signup [ Create a new user ]
@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }