# README

Доброго дня! Цей репозиторій - 

## Installation

To run this project, please follow these steps:

1. Clone the repository to your local machine using the command:
2. Navigate to the project directory in the terminal.
3. Create and activate virtual environment using the following command:

### Linux: 
```
python3 -m venv venv
source venv/bin/activate
```
### Windows: 
```
python -m venv venv
venv\scripts\activate.bat
```
4. Install the required packages using the command:
```
pip install -r requirements.txt
```
5. Run the project using the command:
```
uvicorn main:app
```

## Usage

After running the project, you can access it on http://localhost:8000/. To paraphrase a sentence, you need to send a
request to the `/paraphrase` endpoint with a tree parameter. The tree parameter should be a nltk tree in string format.

Here is an example of a valid url:
```
http://localhost:8000/paraphrase?tree=(S%20(NP%20(NP%20(DT%20The)%20(JJ%20charming)%20(NNP%20Gothic)%20(NNP%20Quarter)%20)%20(,%20,)%20(CC%20or)%20(NP%20(NNP%20Barri)%20(NNP%20G%C3%B2tic)%20)%20)%20(,%20,)%20(VP%20(VBZ%20has)%20(NP%20(NP%20(JJ%20narrow)%20(JJ%20medieval)%20(NNS%20streets)%20)%20(VP%20(VBN%20filled)%20(PP%20(IN%20with)%20(NP%20(NP%20(JJ%20trendy)%20(NNS%20bars)%20)%20(,%20,)%20(NP%20(NNS%20clubs)%20)%20(CC%20and)%20(NP%20(JJ%20Catalan)%20(NNS%20restaurants)%20)%20)%20)%20)%20)%20)%20)
```

The expected response should be similar to the content of the `result.json` file in the repository.