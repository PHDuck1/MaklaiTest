from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to the Tree Paraphraser API"}


@app.get("/paraphrase/{tree}")
async def paraphrase_endpoint(tree: str):
    return {"message": f"Tree received: {tree}"}
