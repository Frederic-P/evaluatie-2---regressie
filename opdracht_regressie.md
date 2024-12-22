# Opdracht: Toepassen van Lineaire Regressie

## Inleiding

In deze opdracht ga je lineaire regressie toepassen op een dataset die informatie bevat over het loon van data profielen. De dataset is beschikbaar in een Excel-bestand met drie tabbladen: `X_train`, `X_test` en `y_train`. Jouw doel is om verschillende regressie modellen te implementeren en hun prestaties te vergelijken.

## Doelstellingen

1. **Data Inlezen en Exploratory Data Analysis (EDA):**
   - Lees de data in vanuit het Excel-bestand.
   - Voer een EDA uit om de data beter te begrijpen. Denk hierbij aan:
     - Het weergeven van een paar rijen van de dataset.
     - Het controleren van missende waarden.
     - Het bekijken van de statistische samenvattingen (bvb correlaties).
     - Het visualiseren van de distributies van belangrijke variabelen.

2. **Implementatie van Regressie Modellen:**
   - Implementeer een aantal verschillende regressie modellen. Denk aan:
     - Lineaire regressie
     - Ridge regressie
     - Lasso regressie
     - Polynomial regressie
   - Zorg ervoor dat je de modellen traint op de trainingsdata (`X_train` en `y_train`).

3. **Vergelijking van Modelprestaties:**
   - Vergelijk de prestaties van de verschillende modellen aan de hand van relevante metrics, zoals:
     - Mean Absolute Error (MAE)
     - Mean Squared Error (MSE)
     - R²-score
   - Maak gebruik van grafieken om de prestaties visueel te vergelijken.

4. **Evaluatie van het Beste Model:**
   - Kies het model met de beste prestaties op de validatie data.
   - Evalueer dit model op de test data (`X_test`).
   - Maak voorspellingen voor de test data en schrijf deze weg naar een bestand genaamd `y_test.csv`. Deze kolom moet dezelfde structuur hebben als die in de sheet `y_train`.

## Verwachte Output

- Een codebase met 1 of meerdere Jupyter Notebooks en/of Python-scripts die bovenstaande stappen uitvoert.
- Een uitvoerbestand `y_test.csv` met de voorspellingen voor de testdata.

**Opgelet:** Zeker bij het gedeelte EDA kan je al snel een soepje krijgen van vanalles en nog wat. Probeer er zeker voor te zorgen dat je aan het einde van de rit je werk opkuist zodat je een mooi geheel kan afleveren.

## Beoordeling

Je opdracht zal worden beoordeeld op de volgende criteria:

- **Data Inzicht:** Kwaliteit van de EDA (30%)
- **Model Implementatie:** Correctheid en variëteit van de regressie modellen (20%)
- **Vergelijking van Modellen:** Duidelijkheid en diepgang van de modelvergelijking (30%)
- **Evaluatie en Output:** Kwaliteit van het gekozen model en het correct wegschrijven van de voorspellingen (20%)