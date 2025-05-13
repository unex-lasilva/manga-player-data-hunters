import pandas as pd

def calcular_suporte(df, itemset):
    subset = df[list(itemset)]
    is_present = subset.all(axis=1)
    suporte = is_present.sum() / len(df)
    return suporte

def gerar_candidatos(frequentes_prev, k):
    candidatos = []
    n = len(frequentes_prev)

    for i in range(n):
        for j in range(i + 1, n):
            conjunto1 = frequentes_prev[i]
            conjunto2 = frequentes_prev[j]

            union = sorted(set(conjunto1).union(set(conjunto2)))

            if len(union) == k and union not in candidatos:
                subconjuntos_validos = True
                for idx in range(len(union)):
                    subset = union[:idx] + union[idx+1:]
                    if subset not in frequentes_prev:
                        subconjuntos_validos = False
                        break
                if subconjuntos_validos:
                    candidatos.append(union)

    return candidatos

def gerar_regras(itemset, suporte_itemset, suporte_dict, min_confidence):
    regras = []
    n = len(itemset)

    for i in range(1, 2 ** n - 1):
        antecedente = []
        consequente = []
        for j in range(n):
            if (i >> j) & 1:
                antecedente.append(itemset[j])
            else:
                consequente.append(itemset[j])

        if not antecedente or not consequente:
            continue

        antecedente_t = tuple(sorted(antecedente))
        consequente_t = tuple(sorted(consequente))
        suporte_antecedente = suporte_dict[antecedente_t]
        suporte_consequente = suporte_dict[consequente_t]

        confidence = suporte_itemset / suporte_antecedente
        lift = confidence / suporte_consequente

        if confidence >= min_confidence:
            regras.append({
                'antecedente': antecedente_t,
                'consequente': consequente_t,
                'support': suporte_itemset,
                'confidence': confidence,
                'lift': lift
            })

    return regras

def apriori(df, min_support, min_confidence):
    itens = df.columns.tolist()
    resultados = []
    suporte_dict = {}

    candidatos = [[item] for item in itens]
    k = 1

    while candidatos:
        frequentes = []
        for itemset in candidatos:
            suporte = calcular_suporte(df, itemset)
            if suporte >= min_support:
                frequentes.append(itemset)
                itemset_t = tuple(sorted(itemset))
                suporte_dict[itemset_t] = suporte
                resultados.append({'itemsets': itemset_t, 'support': suporte})

        k += 1
        candidatos = gerar_candidatos(frequentes, k)

    regras = []
    for entry in resultados:
        itemset = list(entry['itemsets'])
        suporte_itemset = entry['support']

        if len(itemset) >= 2:
            regras_itemset = gerar_regras(itemset, suporte_itemset, suporte_dict, min_confidence)
            regras.extend(regras_itemset)

    return pd.DataFrame(resultados), pd.DataFrame(regras)


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

    return pd.merge(df_movie, df_ratings, left_on='id', right_on='movieId')


def main():
    user_id, recommendation_type = display_menu()
    
    if recommendation_type == '1':
        print(f"\nVocê escolheu: Recomendação baseada no histórico de gostos do usuário {user_id}.")
        recommend_by_history(user_id)
    elif recommendation_type == '2':
        print(f"\nVocê escolheu: Recomendação baseada no último filme que o usuário {user_id} gostou.")
        recommend_by_last_movie(user_id)



if __name__ == "__main__":
    df = import_datas()
    main()
    