from django.shortcuts import render
from django.http import JsonResponse
import urllib.request
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request, pokemon_name):
    if request.method == 'GET':
        try:
            
            pokemon = pokemon_name.lower()
            pokemon = pokemon.replace(' ', '') # Remove espaços
            url_pokeapi = urllib.request.Request(f'https://pokeapi.co/api/v2/pokemon/{pokemon}/')
            url_pokeapi.add_header('User-Agent', 'psyduck') # Adiciona um User-Agent para evitar erro 403

            source = urllib.request.urlopen(url_pokeapi).read()

            lista_de_dados = json.loads(source)

            dados = {
                'Numero': str(lista_de_dados['id']),
                'Nome': str(lista_de_dados['name']).capitalize(),
                'Tipo': [str(tipo['type']['name']) for tipo in lista_de_dados['types']][0],
                'Altura': str(lista_de_dados['height']),
                'Peso': str(lista_de_dados['weight']),
                'Habilidades': [str(ability['ability']['name']) for ability in lista_de_dados['abilities']],
                'Imagem': str(lista_de_dados['sprites']['front_default']),
            }

            return JsonResponse(dados)

        except Exception as e:
          return JsonResponse({'erro': 'Pokemon não encontrado'})
    
    return JsonResponse({'erro': 'Método não permitido'})
