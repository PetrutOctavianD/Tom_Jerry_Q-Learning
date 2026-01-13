# Tom & Jerry Q-Learning 

## Descriere

Acest proiect implementeaza algoritmul Q-Learning, o metoda de invatare prin intarire (Reinforcement Learning), pentru a invata un agent (pisica) sa navigheze intr-un labirint si sa prinda tinta (soarecele).

Agentul invata prin interactiune repetata cu mediul, primind recompense pentru actiuni bune si penalizari pentru actiuni proaste, formand o politica optima de navigare.

## Caracteristici

- Implementare completa a algoritmului Q-Learning

- Mediul de simulare: labirint 8x8 generat procedural

- Vizualizare grafica in timp real cu PyGame

- Sistem de scoruri si statistici

- Parametri configurabili pentru experimentare

- Interfata simpla si intuitiva

## Instalare

1. **Descarca si dezarhiveaza proiectul**

```bash
cd tom-jerry-qlearning
```

2. **Creeaza si activeaza un mediu virtual**

```bash
python -m venv venv
venv\Scripts\activate
```

3. **Instaleaza dependentele**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Ruleaza aplicatia**

Rulare simpla (10 episoade):
```bash
python main.py
```
Rulare cu numar specific de episoade:
```bash
python main.py 20
```

5. **Controale in timpul vizualizarii:**

-SPACE - Pauza/Continua
-ESC - Iesire din program