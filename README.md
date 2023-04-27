# README

### Доброго дня! 
Цей репозиторій - виконане тестове завдання для проходження на стажування в Maklai: https://dou.ua/calendar/46895/?from=first-job
### Виконав Думанський Дмитро

## Installation

To run this project, please follow these steps:

1. Clone the repository to your local machine.
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

After running the project, you can copy next url and paste in into web-browser.

```
http:localhost:8000/paraphrase?tree=(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP
Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP
(JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ
trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS
restaurants) ) ) ) ) ) ) )
```

The expected response should be similar to the content of the `result.json` file in the repository.