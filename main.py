from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SalaryInput(BaseModel):
    heures: float
    heures_dimanche: float


TAUX_HORAIRE = 12.2561      
MAJORATION_DIMANCHE = 7.86

@app.post("/calculate")
def calculate(data: SalaryInput):
    heuresTravaillees = float(input("Heures travaillées: "))
    heuresDimanches = float(input("Heures travaillées le dimanche: "))

    salaireBaseMensu = TAUX_HORAIRE * 151.67
    absenceEntreeSortie = (151.67 - heuresTravaillees) * 13.8253
    salaireBase = salaireBaseMensu - absenceEntreeSortie
    indeminteSujetion = 0.0921 * (heuresTravaillees * 12.2561)
    majorationDimanche =heuresDimanches * MAJORATION_DIMANCHE

    indemnitePrecarite = 0.10* (salaireBase + indeminteSujetion + majorationDimanche +238)
    indemniteCongesPayes = 0.10 * (salaireBase + indeminteSujetion + majorationDimanche + indemnitePrecarite+238)

    salaireBrut = salaireBase + indeminteSujetion + majorationDimanche + indemnitePrecarite + indemniteCongesPayes + 238
    salaireNet = salaireBrut * 0.769


    return {
        "heures_normales": heuresTravaillees - heuresDimanches,
        "heures_dimanche": heuresDimanches,
        "taux_horaire": TAUX_HORAIRE,
        "majoration_dimanche": MAJORATION_DIMANCHE,
        "salaire_net": round(salaireNet, 2),
        "salaire_brut": round(salaireBrut, 2)
    }
