from paraphrase import get_paraphrased_trees
from nltk.tree import Tree
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Tree Paraphraser API by Dumanskyi Dmytro"}


@app.get("/paraphrase")
async def paraphrase_endpoint(tree: str):
    try:
        syntax_tree = Tree.fromstring(tree)
    except ValueError:
        return {
            "error": {
                "code": 400,
                "message": "Invalid value for parameter tree."
            }
        }

    paraphrased_trees = get_paraphrased_trees(syntax_tree)

    return {"paraphrases": paraphrased_trees}
