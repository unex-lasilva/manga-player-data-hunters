import numpy as np
import pandas as pd

def recommend_by_history(user_id):
    # Essa função vai usar o histórico do usuário
    # Vai chamar o algoritmo Apriori
    # Vai trazer recomendações de filmes
    pass

def recommend_by_last_movie(user_id):
    # Essa função vai usar o último filme que o usuário gostou
    # Vai chamar o algoritmo Apriori
    # Vai trazer recomendações de filmes
    pass

def display_menu():
    print("=== Manga Play - Sistema de Recomendação ===")
    user_id = input("Digite o ID do usuário: ")
    print("\nEscolha o tipo de recomendação:")
    print("1 - Baseada no histórico de gostos")
    print("2 - Baseada no último filme gostado")
    option = input("Digite 1 ou 2: ")

    while option not in ['1', '2']:
        print("Opção inválida! Tente novamente.")
        option = input("Digite 1 ou 2: ")

    return user_id, option

def import_datas():
    df_movie = pd.read_csv("../data/movies_metadata.csv", low_memory=False)
    df_movie = df_movie[pd.to_numeric(df_movie['id'], errors='coerce').notna()]
    df_movie['id'] = df_movie['id'].astype(int)
    #
    df_ratings = pd.read_csv("../data/ratings_small.csv", low_memory=False)
    df_ratings['movieId'] = df_ratings['movieId'].astype(int)

    df = pd.merge(df_movie, df_ratings, left_on='id', right_on='movieId')
    pd.set_option('display.max_columns', None)
    print(df)

def main():
    user_id, recommendation_type = display_menu()
    
    if recommendation_type == '1':
        print(f"\nVocê escolheu: Recomendação baseada no histórico de gostos do usuário {user_id}.")
        recommend_by_history(user_id)
    elif recommendation_type == '2':
        print(f"\nVocê escolheu: Recomendação baseada no último filme que o usuário {user_id} gostou.")
        recommend_by_last_movie(user_id)

if __name__ == "__main__":
    import_datas()
    main()
    