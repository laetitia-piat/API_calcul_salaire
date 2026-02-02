from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Autorise Next en local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modèle d'entrée
class SalaryInput(BaseModel):
    heures: float
    heures_dimanche: float

# --- Variables "métier" (à personnaliser)
TAUX_HORAIRE = 25.0          # ex: 25€ / heure
MAJORATION_DIMANCHE = 0.5    # ex: +50% le dimanche

@app.post("/calculate")
def calculate(data: SalaryInput):
    heures_normales = max(0.0, data.heures - data.heures_dimanche)
    h_dim = max(0.0, data.heures_dimanche)

    salaire_normal = heures_normales * TAUX_HORAIRE
    salaire_dimanche = h_dim * TAUX_HORAIRE * (1 + MAJORATION_DIMANCHE)

    total = salaire_normal + salaire_dimanche

    return {
        "heures_normales": heures_normales,
        "heures_dimanche": h_dim,
        "taux_horaire": TAUX_HORAIRE,
        "majoration_dimanche": MAJORATION_DIMANCHE,
        "salaire_normal": round(salaire_normal, 2),
        "salaire_dimanche": round(salaire_dimanche, 2),
        "total": round(total, 2),
    }
