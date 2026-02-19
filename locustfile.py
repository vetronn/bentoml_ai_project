#generovanie záťaźe na model
from locust import HttpUser, task, between
import numpy as np

class BentoMLUser(HttpUser):
    wait_time = between(3, 5)
    @task
    def predict(self):
        # Simulujeme náhodné dáta pre Iris model (4 čísla)
        # Ak máš iný model, uprav si formát dát
        raw_data = np.random.rand(4).tolist()

        #zabalime ich do objektu, ktory model ocakava
        payload = {
            "input_series":[raw_data]
        } 

        self.client.post(
            "/classify", 
            json=payload,
            headers={"Content-Type": "application/json"}
        )
