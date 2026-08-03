import numpy as np
import pandas as pd

class MatrixFactorizationSVD:
    def __init__(self, n_factors=10, lr=0.005, reg=0.02, epochs=35, random_state=42):
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.epochs = epochs
        self.random_state = random_state
        self.mu = 0.0
        self.b_u = None
        self.b_i = None
        self.P = None
        self.Q = None
        self.user_to_idx = {}
        self.idx_to_user = {}
        self.laptop_to_idx = {}
        self.idx_to_laptop = {}
        
    def fit(self, ratings_df):
        """
        Entrena el modelo SVD sobre un DataFrame con columnas: user_id, laptop_id, rating.
        Optimiza mediante Descenso de Gradiente Estocástico (SGD).
        """
        np.random.seed(self.random_state)
        
        # Mapeos de IDs únicos a índices densos (0 a N-1)
        unique_users = ratings_df["user_id"].unique()
        unique_laptops = ratings_df["laptop_id"].unique()
        
        self.user_to_idx = {user: idx for idx, user in enumerate(unique_users)}
        self.idx_to_user = {idx: user for user, idx in self.user_to_idx.items()}
        self.laptop_to_idx = {laptop: idx for idx, laptop in enumerate(unique_laptops)}
        self.idx_to_laptop = {idx: laptop for laptop, idx in self.laptop_to_idx.items()}
        
        n_users = len(unique_users)
        n_items = len(unique_laptops)
        
        # Media global
        self.mu = float(ratings_df["rating"].mean())
        
        # Inicializar sesgos y factores latentes
        self.b_u = np.zeros(n_users)
        self.b_i = np.zeros(n_items)
        self.P = np.random.normal(0, 0.1, (n_users, self.n_factors))
        self.Q = np.random.normal(0, 0.1, (n_items, self.n_factors))
        
        # Mapear los datos de entrenamiento
        train_data = []
        for _, row in ratings_df.iterrows():
            u_idx = self.user_to_idx[row["user_id"]]
            i_idx = self.laptop_to_idx[row["laptop_id"]]
            r = float(row["rating"])
            train_data.append((u_idx, i_idx, r))
            
        # SGD
        for epoch in range(self.epochs):
            # Barajar para convergencia de SGD
            np.random.shuffle(train_data)
            for u, i, r in train_data:
                # Estimación: r_hat = mu + b_u + b_i + P_u . Q_i
                pred = self.mu + self.b_u[u] + self.b_i[i] + np.dot(self.P[u], self.Q[i])
                err = r - pred
                
                # Actualizar sesgos
                self.b_u[u] += self.lr * (err - self.reg * self.b_u[u])
                self.b_i[i] += self.lr * (err - self.reg * self.b_i[i])
                
                # Actualizar matrices P y Q
                p_old = self.P[u].copy()
                self.P[u] += self.lr * (err * self.Q[i] - self.reg * self.P[u])
                self.Q[i] += self.lr * (err * p_old - self.reg * self.Q[i])
                
        print(f"Modelo SVD entrenado sobre {len(ratings_df)} valoraciones.")

    def predict(self, user_id, laptop_id):
        """
        Predice la valoración del usuario u para la laptop i.
        Resuelve el problema de Cold Start si no se conoce el usuario o la laptop.
        """
        u_seen = user_id in self.user_to_idx
        i_seen = laptop_id in self.laptop_to_idx
        
        if u_seen and i_seen:
            u_idx = self.user_to_idx[user_id]
            i_idx = self.laptop_to_idx[laptop_id]
            pred = self.mu + self.b_u[u_idx] + self.b_i[i_idx] + np.dot(self.P[u_idx], self.Q[i_idx])
        elif i_seen:
            # Usuario Cold Start (Nuevo): se usa el sesgo global + sesgo del item
            i_idx = self.laptop_to_idx[laptop_id]
            pred = self.mu + self.b_i[i_idx]
        elif u_seen:
            # Laptop Cold Start (Nueva): se usa el sesgo global + sesgo del usuario
            u_idx = self.user_to_idx[user_id]
            pred = self.mu + self.b_u[u_idx]
        else:
            # Caso extremo de ambos no vistos
            pred = self.mu
            
        return float(np.clip(pred, 1.0, 5.0))

    def predict_normalized(self, user_id, laptop_id):
        """
        Retorna la calificación predicha escalada en el intervalo [0, 1].
        Útil para el ensamble dinámico del sistema híbrido.
        """
        pred = self.predict(user_id, laptop_id)
        # Escala original 1-5 a 0-1
        return (pred - 1.0) / 4.0
